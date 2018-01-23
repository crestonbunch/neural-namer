import * as React from "react";
import { Button, Container, Grid, Icon, Segment } from "semantic-ui-react";
import { Array2D, ENV, NDArrayMath, Scalar } from "deeplearn";
import Network from "../../model/network";

import Weights from "./Weights";

interface GeneratorProps {
  onGenerate: (name: string, weights: Map<string, number>) => void;
}

interface GeneratorState {
  disabled: boolean;
  weights: Map<string, number>;
}

export default class Generator extends React.PureComponent<
  GeneratorProps,
  GeneratorState
> {
  state: GeneratorState;
  network: Network;
  constructor(props) {
    super(props);
    this.state = {
      disabled: false,
      weights: new Map<string, number>([
        ["Tolkien", 1.0],
        ["George Martin", 0.0],
        ["Robert Jordan", 0.0],
        ["Steven Erikson", 0.0],
        ["Brian Jacques", 0.0],
        ["Frank Herbert", 0.0],
        ["Andrzej Sapkowski", 0.0]
      ])
    };
    this.network = new Network();
  }
  onGenerate = async () => {
    this.setState({ disabled: true });

    const math = ENV.math;

    return await math.scope(async () => {
      await this.network.init("./vars");
      const name = await this.network.generate(
        math,
        await this.getEmbedding(math)
      );
      this.setState({ disabled: false });
      this.props.onGenerate(name, this.state.weights);
    });
  };
  onWeightsChange = (weights: Map<string, number>) => {
    this.setState({
      weights
    });
  };
  /**
   * Computes the input author embedding by weighting the vectors for each
   * author.
   */
  getEmbedding = async (math: NDArrayMath): Promise<Array2D> => {
    let vectorPromises: Array<Promise<Array2D>> = [];
    this.state.weights.forEach((weight, author) => {
      vectorPromises.push(
        this.network.embedAuthor(author).then(vec => {
          return math.multiply(vec as any, Scalar.new(weight)) as any;
        })
      );
    });
    const vecs = await Promise.all(vectorPromises);
    return vecs.reduce((prev, vec) => {
      if (prev === null) {
        return vec;
      }
      return math.add(prev, vec);
    }, null);
  };
  render() {
    return (
      <>
        <Segment attached="top">
          <Weights
            weights={this.state.weights}
            onChange={this.onWeightsChange}
          />
        </Segment>
        <Button
          attached="bottom"
          disabled={this.state.disabled}
          loading={this.state.disabled}
          fluid
          onClick={this.onGenerate}
          primary
          positive
          size="large"
        >
          Generate
        </Button>
      </>
    );
  }
}
