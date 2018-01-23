import {
  Array1D,
  Array2D,
  CheckpointLoader,
  ENV,
  LSTMCell,
  NDArrayMath,
  Scalar
} from "deeplearn";
import { contextWrapper } from "./context";

const MAX_LEN = 100;

export default class Network {
  authorMap: Object;
  characterEmbedding: Array2D;
  characterMap: Object;
  contextEmbedding: Array2D;
  contextOutputBias: Array1D;
  contextOutputKernel: Array2D;
  contextStateBias: Array1D;
  contextStateKernel: Array2D;
  indexMap: Object;
  LSTMBias: Array1D;
  LSTMKernel: Array2D;
  outBias: Array1D;
  outKernel: Array2D;
  /**
   * Initializes the network using the saved variables.
   */
  async init(checkpoint) {
    this.authorMap = await (await fetch(
      `${checkpoint}/author_map.json`
    )).json();
    this.characterMap = await (await fetch(
      `${checkpoint}/vocab_map.json`
    )).json();
    this.indexMap = await (await fetch(`${checkpoint}/index_map.json`)).json();
    const loader = new CheckpointLoader(checkpoint);
    const vars = await loader.getAllVariables();
    this.characterEmbedding = vars["char_embedding"] as Array2D;
    this.contextEmbedding = vars["ctx_embedding"] as Array2D;
    this.outKernel = vars["decoder/fully_connected/kernel"] as Array2D;
    this.outBias = vars["decoder/fully_connected/bias"] as Array1D;
    this.LSTMKernel = vars[
      "decoder/multi_rnn_cell/cell_0/basic_lstm_cell/kernel"
    ] as Array2D;
    this.LSTMBias = vars[
      "decoder/multi_rnn_cell/cell_0/basic_lstm_cell/bias"
    ] as Array1D;
    this.contextOutputBias = vars[
      "decoder/multi_rnn_cell/cell_0/output_ctx/bias"
    ] as Array1D;
    this.contextOutputKernel = vars[
      "decoder/multi_rnn_cell/cell_0/output_ctx/kernel"
    ] as Array2D;
    this.contextStateBias = vars[
      "decoder/multi_rnn_cell/cell_0/state_ctx/bias"
    ] as Array1D;
    this.contextStateKernel = vars[
      "decoder/multi_rnn_cell/cell_0/state_ctx/kernel"
    ] as Array2D;
  }
  /**
   * Generate a name using the given context vector. Should be called within
   * a math scope along with init() to avoid any arrays being automatically
   * disposed.
   *
   * @param contextVector An embedded author vector whose style to emulate.
   */
  async generate(math: NDArrayMath, contextVector: Array2D): Promise<string> {
    const results: string[] = [];
    const LSTMCell = math.basicLSTMCell.bind(
      math,
      Scalar.new(1.0),
      this.LSTMKernel,
      this.LSTMBias
    );
    const contextCell = contextWrapper.bind(
      math,
      this.contextStateKernel,
      this.contextStateBias,
      this.contextOutputKernel,
      this.contextOutputBias,
      LSTMCell,
      contextVector
    );
    let c = [Array2D.zeros([1, this.LSTMBias.shape[0] / 4])];
    let h = [Array2D.zeros([1, this.LSTMBias.shape[0] / 4])];
    let prime = await this.embedCharacter("\u25B6");
    for (let i = 0; i < MAX_LEN; i++) {
      const batch = prime;
      const LSTMState = math.multiRNNCell([contextCell], prime, c, h);
      const cellState = LSTMState[0];
      const hiddenState = LSTMState[1];
      const output = hiddenState[0];
      const logits = math.relu(
        math.add(math.matMul(output, this.outKernel), this.outBias)
      );
      const softmax = math.softmax(logits.as1D());
      const sampledOutput = await math
        .multinomial(softmax, 1)
        .asScalar()
        .val();
      const characterOutput = this.indexMap[sampledOutput];
      if (characterOutput === "\u25C0") {
        break;
      }
      const result = results.push(characterOutput);
      c = cellState;
      h = hiddenState;
      prime = await this.embedCharacter(characterOutput);
    }

    return results.join("");
  }
  /**
   * Return the character embedding for a single character.
   *
   * @param char The character to lookup.
   */
  async embedCharacter(char: string): Promise<Array2D> {
    const math = ENV.math;
    return await math.scope(() => {
      const index = this.characterMap[char];
      const size = this.characterEmbedding.shape[1];
      return math.slice2D(this.characterEmbedding, [index, 0], [1, size]);
    });
  }
  /**
   * Return the vector embedding for a given author.
   *
   * @param author The name of the author to lookup
   */
  async embedAuthor(author: string): Promise<Array2D> {
    const math = ENV.math;
    return await math.scope(() => {
      const index = this.authorMap[author];
      const size = this.contextEmbedding.shape[1];
      return math.slice2D(this.contextEmbedding, [index, 0], [1, size]);
    });
  }
}
