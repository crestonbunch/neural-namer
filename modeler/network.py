import tensorflow as tf
from tensorflow.contrib.rnn import MultiRNNCell, DeviceWrapper, DropoutWrapper
from tensorflow.contrib.seq2seq import \
    BasicDecoder, TrainingHelper, SampleEmbeddingHelper, dynamic_decode
from modeler.context import ContextWrapper

CELLS = {
    'gru': tf.contrib.rnn.GRUCell,
    'lstm': tf.contrib.rnn.BasicLSTMCell,
    'rnn': tf.contrib.rnn.BasicRNNCell
}
ACTIVATIONS = {
    'relu': tf.nn.relu,
    'sigmoid': tf.nn.sigmoid,
    'tanh': tf.nn.tanh
}

class Network:

    def __init__(self, seq, labels, contexts, vocab_size, author_size, **kwargs):
        self._vocab_size = vocab_size
        self._author_size = author_size
        self._input_dropout = kwargs.get('input_dropout', 0.0)
        self._output_dropout = kwargs.get('output_dropout', 0.0)
        self._cell = CELLS.get(kwargs.get('cell'), CELLS['lstm'])
        self._cell_size = kwargs.get('cell_size', 128)
        self._cell_num = kwargs.get('cell_num', 1)
        self._embed_size = kwargs.get('embed_size', 32)
        self._ctx_size = kwargs.get('ctx_size', 2)
        self._activation = ACTIVATIONS.get(kwargs.get('activation'), tf.nn.tanh)
        self._training = kwargs.get('training', True)
        self._num_gpu = kwargs.get('num_gpu', 1)

        self.target_node, self.loss_node, self.out_node = self._init(seq, labels, contexts)

    def _init(self, sequence, targets, authors):
        batch_size = tf.shape(sequence)[0]

        sequence_lengths = tf.cast(tf.count_nonzero(sequence, axis=1), tf.int32)
        embedding = tf.Variable(
            tf.random_normal((self._vocab_size, self._embed_size)),
            name='char_embedding'
        )
        context = tf.Variable(
            tf.random_normal((self._author_size, self._ctx_size)),
            name='ctx_embedding'
        )

        embedded_sequence = tf.nn.embedding_lookup(embedding, sequence)
        embedded_authors = tf.nn.embedding_lookup(context, authors)

        gpu = lambda x: '/gpu:{}'.format(x % self._num_gpu)

        if self._training:
            dropout = lambda x: DropoutWrapper(
                x, 1.0-self._input_dropout, 1.0-self._output_dropout)
            helper = TrainingHelper(embedded_sequence, sequence_lengths)
        else:
            dropout = lambda x: x
            helper = SampleEmbeddingHelper(embedding, sequence[:,0], 2)

        base = lambda x: ContextWrapper(self._cell(x), embedded_authors)
        wrap = lambda i, cell: DeviceWrapper(dropout(cell), gpu(i))
        cells = [wrap(i, base(self._cell_size)) for i in range(self._cell_num)]
        cell = MultiRNNCell(cells)

        init_state = cell.zero_state(batch_size, tf.float32)
        dense = tf.layers.Dense(
            self._vocab_size, self._activation, name='fully_connected'
        )
        decoder = BasicDecoder(cell, helper, init_state, dense)
        output, _, _ = dynamic_decode(decoder, swap_memory=True)
        logits = output.rnn_output

        weights = tf.sequence_mask(sequence_lengths, dtype=tf.float32)
        loss = tf.contrib.seq2seq.sequence_loss(
            logits,
            targets,
            weights
        )

        out = output.sample_id

        return targets, loss, out
