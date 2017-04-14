import math
import numpy as np
import tensorflow as tf
from modeler.context_cell import ContextRNNCell
from tensorflow.contrib.rnn import GRUCell, LSTMCell, MultiRNNCell

def init_network(vocab_size, author_size, num_hidden, num_cells):
    """Initialize an untrained network."""

    sequence = tf.placeholder(tf.int32, [None, None], name='sequence')
    targets = tf.placeholder(tf.int32, [None, None], name='targets')
    authors = tf.placeholder(tf.int32, [None, None], name='authors')

    # one hots are (batch_size, max_length, feature_len)
    one_hot_sequence = tf.one_hot(sequence, vocab_size, axis=-1)
    one_hot_targets = tf.one_hot(targets, vocab_size, axis=-1)
    one_hot_authors = tf.one_hot(authors, author_size, axis=-1)

    batch_size = tf.shape(sequence)[0]
    max_length = tf.shape(sequence)[1]

    cell = MultiRNNCell([ContextRNNCell(num_hidden, author_size) for _ in range(num_cells)])
    init_state = cell.zero_state(batch_size, tf.float32)

    inputs = tf.concat([one_hot_sequence, one_hot_authors], axis=2)

    # output is (batch_size, max_length, num_hidden)
    output, state = tf.nn.dynamic_rnn(
        cell,
        inputs,
        dtype=tf.float32,
        initial_state = init_state,
        sequence_length=length(sequence),
    )

    # output is (batch_size * max_length, num_hidden)
    reshaped_output = tf.reshape(output, [-1, num_hidden])
    reshaped_authors = tf.reshape(one_hot_authors, [-1, author_size])

    V = tf.Variable(
        tf.truncated_normal((num_hidden, vocab_size), stddev=1.0/math.sqrt(vocab_size))
    )
    G = tf.Variable(
        tf.truncated_normal((author_size, vocab_size), stddev=1.0/math.sqrt(vocab_size))
    )
    b = tf.Variable(tf.fill((vocab_size,), 0.1))

    # logits is shape (batch_size * max_length, vocab_size)
    logits = tf.matmul(reshaped_output, V) + tf.matmul(reshaped_authors, G) + b
    # logits is shape (batch_size, max_length, vocab_size)
    logits = tf.reshape(logits, (batch_size, max_length, vocab_size))
    # probs is shape (batch_size, max_length, vocab_size)
    probs = tf.nn.softmax(logits)

    loss = tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=one_hot_targets
    )
    loss = tf.reduce_mean(loss)

    return sequence, targets, authors, loss, cell, init_state, state, probs

def length(sequence):
    """Compute the length of a zero-padded sequence by ignoring the 0's."""
    return tf.count_nonzero(sequence, axis=1)

def cost(labels=None, logits=None):
    """Compute the cross entropy of the output with the target."""
    vocab_size = tf.shape(logits)[1]
    mask = tf.cast(tf.sign(tf.reshape(labels, (-1, 1))), tf.float32)
    labels = tf.reshape(tf.one_hot(labels, vocab_size), (-1, vocab_size))
    logits = tf.cast(logits, tf.float32)
    cross_entropy = -(labels * tf.log(logits)) * tf.tile(mask, [1, vocab_size])
    cross_entropy = tf.reduce_sum(cross_entropy, axis=1)
    return tf.reduce_mean(cross_entropy)

def last_relevant(output, length):
    """Select the last relevant frame of the output to feed to classifier."""
    batch_size = tf.shape(output)[0]
    max_length = tf.shape(output)[1]
    out_size = int(output.get_shape()[2])
    index = tf.range(0, batch_size) * max_length + (length - 1)
    flat = tf.reshape(output, [-1, out_size])
    relevant = tf.gather(flat, index)
    return relevant

def sample(
    sess, seq_node, author_node, cell_node, init_node, state_node, 
    prob_node, author, lookup, reverse_lookup
):
    """Sample a sequence from a trained model."""
    last_char = 0
    seq = ''
    state = sess.run(cell_node.zero_state(1, tf.float32))
    while last_char != lookup['']:
        mapped_seq = [[lookup[c] for c in seq]] if seq else [[1]]
        mapped_auth = [[author] * len(mapped_seq[0])]
        probs, state = sess.run([prob_node, state_node], {
            seq_node: mapped_seq,
            init_node: state,
            author_node: mapped_auth
        })

        p = probs[0][-1]
        last_char = weighted_pick(p)
        seq += reverse_lookup[last_char] if last_char > 0 else ''

    return seq

def weighted_pick(weights):
    """Pick an index randomly based on weight."""
    t = np.cumsum(weights)
    s = np.sum(weights)
    return(int(np.searchsorted(t, np.random.rand(1)*s)))