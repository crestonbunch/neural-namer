import os
import pickle
import random
import tensorflow as tf

import modeler.model as model
import modeler.sampling as sampling
from modeler.parameters import BATCH_SIZE, NUM_HIDDEN, LEARN_RATE, NUM_EPOCHS, \
    NUM_CELLS

def train(infile, logdir):
    """Train a model with the given input data file."""

    with open(infile, 'rb') as file_handler:
        samples, authors = pickle.load(file_handler)
        vocab_size = max(max(samples))
        author_size = max(authors) + 1

    seq_node, target_node, author_node, loss_node, _, _, _, _ = model.init_network(
        vocab_size, author_size, NUM_HIDDEN, NUM_CELLS
    )

    train_step = tf.train.AdamOptimizer(LEARN_RATE).minimize(loss_node)

    tf.summary.scalar('loss', loss_node)

    sess = tf.Session()

    with tf.name_scope('saver'):
        saver = tf.train.Saver()
        summaries = tf.summary.merge_all()
        writer = tf.summary.FileWriter(logdir, sess.graph)

    sess.run(tf.global_variables_initializer())

    checkfile = os.path.join(logdir, 'model.ckpt')

    step = 0
    for epoch in range(1, NUM_EPOCHS+1):
        sample_gen = sampling.batch_samples(samples, authors, BATCH_SIZE)
        for batch in sample_gen:
            sequence, target, auths = batch

            err, summary, _, _, _ = sess.run(
                [loss_node, summaries, train_step, seq_node, target_node],
                feed_dict={
                    seq_node: sequence,
                    target_node: target,
                    author_node: auths,
                }
            )

            print('Epoch: ', epoch, 'Loss: ', err)
            writer.add_summary(summary, step)
            if step % 1000 == 0:
                saver.save(sess, os.path.join(checkfile), step)
                print('Checkpoint saved.')
            step += 1

    saver.save(sess, os.path.join(checkfile), step)
    print('Checkpoint saved.')
