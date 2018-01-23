import * as React from "react";
import {
  Button,
  Container,
  Divider,
  Header,
  Statistic
} from "semantic-ui-react";
import { Link } from "react-router-dom";

import Names from "./Names";

interface PreviewProps {
  match: {
    params: {
      name: string;
      weights: string;
    };
  };
}

interface PreviewState {
  weights: Map<string, number>;
}
export default class Preview extends React.PureComponent<
  PreviewProps,
  PreviewState
> {
  state: PreviewState;
  constructor(props) {
    super(props);
    const weights = new Map<string, number>(
      JSON.parse(atob(this.props.match.params.weights)).map(
        ([name, weight]) => [name, parseFloat(weight)]
      )
    );
    console.log(weights);
    this.state = {
      weights
    };
  }
  render() {
    return (
      <Container fluid textAlign="center">
        <Header size="medium">The name</Header>
        <Header size="huge">{this.props.match.params.name}</Header>
        <Header size="medium">is</Header>
        {Array.from(this.state.weights).map(([name, weight]) => (
          <Statistic key={name}>
            <Statistic.Value>{`${(weight * 100).toFixed(0)}%`}</Statistic.Value>
            <Statistic.Label>{name}</Statistic.Label>
          </Statistic>
        ))}
        <Divider hidden />
        <Link to="/">
          <Button primary size="big">
            Generate your own
          </Button>
        </Link>
      </Container>
    );
  }
}
