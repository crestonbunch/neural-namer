"""A contextual RNN cell as described in 
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/rnn_ctxt.pdf"""

import tensorflow as tf
import math
from tensorflow.contrib.rnn import BasicRNNCell, BasicLSTMCell

class ContextRNNCell(BasicRNNCell):
    """A basic RNN cell that implements context as described in the paper
    above. The inputs to the RNN must be concatenated vectors [input, context],
    and the context part will be sliced out and used separately."""

    def __init__(self, num_units, num_context, activation=tf.tanh):
        # set the activation to the identity so we can overwrite the steps
        # before it
        super().__init__(num_units, activation=tf.identity)
        self._num_context = num_context
        self._real_activation = activation
        self.F = tf.Variable(
            tf.truncated_normal((num_context, num_units), stddev=1.0/math.sqrt(num_units))
        )

    def __call__(self, inputs, state, scope=None):
        # splits inputs into context and input parts
        context = inputs[:,-self._num_context:]
        inputs = inputs[:,:-self._num_context]
        state, _ = super().__call__(inputs, state, scope)
        # hijack the RNN implementation just before it does the activation function
        output = self._real_activation(tf.matmul(context, self.F) + state)
        return output, output
