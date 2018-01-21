"""Generate a sequence from a trained model."""

import os
import pickle
import tensorflow as tf
import numpy as np
import random
import string

from modeler.network import Network

def gen(savedir, lookupfile, datafile, author, num):
    """Generate a sequence from the model stored in the logdir."""

    with open('{}.meta'.format(datafile), 'rb') as file_handler:
        vocab_map, _, author_map = pickle.load(file_handler)
        vocab_size = len(vocab_map)
        author_size = len(author_map)

        index_map = {i: char for char, i in vocab_map.items()}

    with open(os.path.join(savedir, 'params.pkl'), 'rb') as file_handler:
        params = pickle.load(file_handler)

    sequences = tf.placeholder(tf.int32, [None, None])
    labels = tf.placeholder(tf.int32, [None, None])
    contexts = tf.placeholder(tf.int32, [None, None])
    network = Network(
        sequences,
        labels,
        contexts,
        vocab_size,
        author_size,
        **vars(params),
        training=False,
    )

    config = tf.ConfigProto(allow_soft_placement=True)
    with tf.Session(config=config) as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(savedir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

            names = []

            seed = '▶'
            seq = [[vocab_map[seed]]] * num
            auth = [[author_map[author]]] * num
            out, = sess.run([network.out_node], {
                sequences: seq,
                contexts: auth,
            })
            for seq in out:
                name = ''.join([index_map.get(x) for x in seq])
                if '◀' in name:
                    names.append(name[:name.index('◀')])
                else:
                    names.append(name)

            return names
        else:
            raise Exception('Checkpoint not found')
