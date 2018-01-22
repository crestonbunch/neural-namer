import { Array1D, Array2D, NDArrayMath, LSTMCell } from "deeplearn";

/**
 * Wraps an LSTM cell to provide context weighting
 *
 * @param state_kernel Kernel for the state context
 * @param state_bias Bias for the state context
 * @param output_kernel Kernel for the output context
 * @param output_bias Bias for the output context
 * @param cell The LSTMCell to wrap
 * @param context The context vector to use
 * @param data The input to the cell
 * @param c Previous cell state
 * @param h Previous cell output
 * @return Tuple [nextCellState, cellOutput]
 */
export function contextWrapper(
  state_kernel: Array2D,
  state_bias: Array1D,
  output_kernel: Array2D,
  output_bias: Array1D,
  cell: LSTMCell,
  context: Array2D,
  data: Array2D,
  c: Array2D,
  h: Array2D
): [Array2D, Array2D] {
  const res = this.scope(() => {
    const output = cell(data, c, h);
    const cellState = output[0];
    const cellOutput = output[1];
    const concatState = this.concat2D(cellState, context, 1);
    const contextState = this.add(
      this.matMul(concatState, state_kernel),
      state_bias
    );
    const concatOutput = this.concat2D(cellOutput, context, 1);
    const contextOutput = this.add(
      this.matMul(concatOutput, output_kernel),
      output_bias
    );

    return [contextState, contextOutput];
  });
  return [res[0], res[1]];
}
