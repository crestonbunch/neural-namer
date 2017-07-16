import tensorflow as tf
from tensorflow.contrib.rnn import MultiRNNCell, BasicLSTMCell, GRUCell, \
    DeviceWrapper, DropoutWrapper
from tensorflow.contrib.seq2seq import \
    BasicDecoder, TrainingHelper, SampleEmbeddingHelper, dynamic_decode, \
    LuongAttention, BahdanauAttention, AttentionWrapper
from tensorflow.python.layers.core import Dense
from modeler.context import ContextWrapper

class Network:

    def __init__(self, vocab_size, author_size, **kwargs):
        self._vocab_size = vocab_size
        self._author_size = author_size
        self._dropout = kwargs['dropout'] if 'dropout' in kwargs else 0.0
        self._cell = kwargs['cell'] if 'cell' in kwargs else 'lstm'
        self._cell_size = kwargs['cell_size'] if 'cell_size' in kwargs else 128
        self._cell_num = kwargs['cell_num'] if 'cell_num' in kwargs else 1
        self._embed_size = kwargs['embed_size'] if 'embed_size' in kwargs else 64
        self._ctx_size = kwargs['ctx_size'] if 'ctx_size' in kwargs else 64
        self._attn = kwargs['attn'] if 'attn' in kwargs else False
        self._attn_depth = kwargs['attn_depth'] if 'attn_depth' in kwargs else 128 
        self._attn_size = kwargs['attn_size'] if 'attn_size' in kwargs else 128
        self._activation = kwargs['activation'] if 'activation' in kwargs else tf.nn.relu
        self._training = kwargs['training'] if 'training' in kwargs else True
        self._num_gpu = kwargs['num_gpu'] if 'num_gpu' in kwargs else 1

        self.seq_node, self.auth_node, self.target_node, self.loss_node, \
            self.out_node = self._init()

    def _init(self):
        sequence = tf.placeholder(tf.int32, [None, None], name='sequence')
        targets = tf.placeholder(tf.int32, [None, None], name='targets')
        authors = tf.placeholder(tf.int32, [None, None], name='authors')

        batch_size = tf.shape(sequence)[0]

        sequence_lengths = tf.cast(tf.count_nonzero(sequence, axis=1), tf.int32)
        embedding = tf.Variable(tf.random_normal((self._vocab_size, self._embed_size)))
        context = tf.Variable(tf.random_normal((self._author_size, self._ctx_size)))

        embedded_sequence = tf.nn.embedding_lookup(embedding, sequence)
        embedded_authors = tf.nn.embedding_lookup(context, authors)
        one_hot_targets = tf.one_hot(targets, self._vocab_size)

        gpu = lambda x: str(x % self._num_gpu)

        if self._attn:
            mech = BahdanauAttention(
                self._attn_depth, embedded_sequence, sequence_lengths
            )
            attn_cell = lambda x: DeviceWrapper(AttentionWrapper(
                x, mech, self._attn_size
            ), "/gpu:" + gpu(1))
        else:
            attn_cell = lambda x: x

        if self._training:
            dropout = lambda x: DropoutWrapper(x, 1.0, 1.0-self._dropout)
        else:
            dropout = lambda x: x

        if self._cell == 'lstm':
            base_cell = lambda x: dropout(BasicLSTMCell(x))
        elif self._cell == 'gru':
            base_cell = lambda x: dropout(GRUCell(x))

        context_cell = ContextWrapper(
            base_cell(self._cell_size), embedded_authors,
        )
        #context_cell = base_cell(self._cell_size)
        bottom_cell = DeviceWrapper(attn_cell(context_cell), "/gpu:0")
        top_cells = [
            DeviceWrapper(base_cell(self._cell_size), "/gpu:" + gpu(i)) 
            for i in range(1, self._cell_num)
        ]
        cell = MultiRNNCell([bottom_cell] + top_cells)

        init_state = cell.zero_state(batch_size, tf.float32)

        if self._training:
            helper = TrainingHelper(embedded_sequence, sequence_lengths)
        else:
            helper = SampleEmbeddingHelper(embedding, sequence[:,0], 1)

        dense = Dense(self._vocab_size, self._activation)
        decoder = BasicDecoder(cell, helper, init_state, dense)
        output, state, _ = dynamic_decode(decoder, swap_memory=True)
        logits = output.rnn_output

        loss = tf.nn.softmax_cross_entropy_with_logits(
            logits=logits, labels=one_hot_targets
        )
        loss = tf.reduce_mean(loss)

        out = tf.nn.softmax(logits)

        return sequence, authors, targets, loss, out
