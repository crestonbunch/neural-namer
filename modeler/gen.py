"""Generate a sequence from a trained model."""

import pickle
import tensorflow as tf

import modeler.model as model

from modeler.parameters import BATCH_SIZE, NUM_HIDDEN, LEARN_RATE, NUM_EPOCHS, \
    NUM_CELLS

def gen(infile, logdir, lookupfile, author, num):
    """Generate a sequence from the model stored in the logdir."""

    with open(infile, 'rb') as file_handler:
        samples, authors = pickle.load(file_handler)
        vocab_size = max(max(samples))
        author_size = max(authors) + 1

    with open(lookupfile, 'rb') as file_handler:
        lookup, reverse_lookup, author_lookup, _ = pickle.load(file_handler)
        author = author_lookup[author]

    seq_node, _, author_node, _, cell_node, init_node, state_node, probs_node = \
    model.init_network(
        vocab_size, author_size, NUM_HIDDEN, NUM_CELLS
    )

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(logdir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            for i in range(num):
                print(model.sample(
                    sess, seq_node, author_node, cell_node, init_node,
                    state_node, probs_node, author, lookup, reverse_lookup
                ))
