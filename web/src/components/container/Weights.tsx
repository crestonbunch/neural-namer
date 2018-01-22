import * as React from "react";
import { Input, Grid } from "semantic-ui-react";

interface WeightsProps {
  onChange: (weights: Map<string, number>) => void;
  weights: Map<string, number>;
}

export default class Weights extends React.PureComponent<WeightsProps, {}> {
  onChange = (key: string, val: number) => {
    const weights = new Map<string, number>(this.props.weights);
    if (weights.get(key) === 1.0) {
      // Disable sliders that are maxed out
      return weights;
    }
    weights.set(key, val);
    const sum = Array.from(weights.values()).reduce((p, c) => p + c);
    const diff = sum - 1.0;
    const order = Array.from(weights.keys()).sort(
      (a, b) => Math.sign(diff) * (weights.get(b) - weights.get(a))
    );
    order
      // Filter out the weight changed by the user
      .filter(k => k !== key)
      // Filter out weights that we can't steal any slack from
      .filter(
        k =>
          (diff > 0 && weights.get(k) > 0) ||
          (diff < 0 && weights.get(k) > 0 && weights.get(k) < 1)
      )
      // Take or add slack to weights as necessary
      .forEach((key, index, arr) => {
        const slack = diff / arr.length;
        const val = Math.min(Math.max(weights.get(key) - slack, 0.0), 1.0);
        weights.set(key, val);
      });
    this.props.onChange(weights);
  };
  render() {
    const rows = [];
    this.props.weights.forEach((weight, name) => {
      rows.push(
        <Grid.Row key={name} verticalAlign="middle">
          <Grid.Column textAlign="left" verticalAlign="middle" width={7}>
            {name}
          </Grid.Column>
          <Grid.Column textAlign="left" verticalAlign="middle" width={6}>
            <Input
              fluid
              transparent
              type="range"
              min={0}
              max={1.0}
              step="any"
              onChange={e => this.onChange(name, e.currentTarget.valueAsNumber)}
              value={weight}
            />
          </Grid.Column>
          <Grid.Column textAlign="left" verticalAlign="middle" width={3}>
            {`${(weight * 100).toFixed(0)}%`}
          </Grid.Column>
        </Grid.Row>
      );
    });
    return <Grid>{rows}</Grid>;
  }
}
