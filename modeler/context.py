"""A contextual RNN cell as described in 
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/rnn_ctxt.pdf"""

import tensorflow as tf
import math
from collections import namedtuple
from tensorflow.contrib.rnn import RNNCell

class ContextState(namedtuple("ContextState", ("cell_state", "time"))):
    def clone(self, **kwargs):
        return super()._replace(**kwargs)

class ContextWrapper(RNNCell):
    """Wraps an RNN cell with context."""

    def __init__(self, cell, context, activation=tf.nn.relu):
        super().__init__()
        self._cell = cell
        self._context = context
        self._activation = activation

    @property
    def output_size(self):
        return self._cell.output_size

    @property
    def state_size(self):
        return ContextState(
            time=tf.TensorShape([]), cell_state=self._cell.state_size
        )

    def zero_state(self, batch_size, dtype):
        return ContextState(
            time=tf.zeros([], dtype=tf.int32),
            cell_state=self._cell.zero_state(batch_size, dtype)
        )

    def __call__(self, inputs, state, scope=None):
        cell_state, cell_output = self._cell(inputs, state.cell_state, scope)

        context_len = tf.shape(self._context)[1]

        context_state = self._activation(tf.layers.dense(
            self._context[:, state.time % context_len, :], self._cell.state_size
        ) + cell_state)

        context_output = self._activation(tf.layers.dense(
            self._context[:, state.time % context_len, :], self._cell.output_size
        ) + tf.layers.dense(
            cell_output, self._cell.output_size
        ))

        return context_output, ContextState(
            time=state.time + 1,
            cell_state=context_state
        )
