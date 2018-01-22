"""A wrapper for an RNN cell that encodes context."""

import tensorflow as tf
import math
from collections import namedtuple
from tensorflow.contrib.rnn import RNNCell, LSTMStateTuple


class ContextState(namedtuple("ContextState", ("cell_state", "time"))):
    def clone(self, **kwargs):
        return super()._replace(**kwargs)


class ContextWrapper(RNNCell):
    """Wraps an RNN cell with context."""

    def __init__(self, cell, context, activation=tf.identity):
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
        with tf.name_scope('context_cell'):
            cell_output, cell_state = self._cell(
                inputs, state.cell_state, scope)
            context_len = tf.shape(self._context)[1]
            context_input = self._context[:, state.time % context_len, :]

            # First we apply context weighting to the cell output
            output_size = self._cell.output_size
            context_output = tf.concat([cell_output, context_input], axis=1)
            context_layer = tf.layers.dense(
                context_output, output_size, name='output_ctx')
            context_output = self._activation(context_layer)

            # Next we add context weighting to the cell state
            if isinstance(self._cell.state_size, LSTMStateTuple):
                # For LSTM cells we only apply context to the cell state
                state_size = self._cell.state_size.c
                context_state = tf.concat(
                    [cell_state.c, context_input], axis=1)
                context_layer = tf.layers.dense(
                    context_state, state_size, name='state_ctx')
                context_state = LSTMStateTuple(
                    c=self._activation(context_layer),
                    h=context_output
                )
            else:
                state_size = self._cell.state_size
                context_state = tf.concat([cell_state, context_input], axis=1)
                context_layer = tf.layers.dense(
                    context_state, state_size, name='state_ctx')
                context_state = self._activation(context_layer)

            return context_output, ContextState(
                time=state.time + 1,
                cell_state=context_state
            )
