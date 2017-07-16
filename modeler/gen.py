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

    with open(datafile, 'rb') as file_handler:
        samples, authors = pickle.load(file_handler)
        vocab_size = max(max(samples))
        author_size = max(authors) + 1

    with open(lookupfile, 'rb') as file_handler:
        lookup, reverse_lookup, author_lookup, _ = pickle.load(file_handler)
        author = author_lookup[author]

    with open(os.path.join(savedir, 'params.pkl'), 'rb') as file_handler:
        params = pickle.load(file_handler)

    params.training = False
    network = Network(vocab_size, author_size, **vars(params))

    config = tf.ConfigProto(allow_soft_placement=True)
    with tf.Session(config=config) as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(savedir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

            names = []

            for _ in range(num):
                seed = random.choice(string.ascii_uppercase)
                seq = [[lookup[seed]]]
                auth = [[author]]
                out = sess.run([network.out_node], {
                    network.seq_node: seq,
                    network.auth_node: auth,
                })
                
                seq = list(np.squeeze(np.argmax(out, axis=3)))
                names.append(seed + ''.join([reverse_lookup[x] if x != 0 else '' for x in seq]))

            return names
        else:
            raise Exception('Checkpoint not found')
