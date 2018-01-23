import * as React from "react";

import Generator from "./Generator";
import Names from "./Names";

interface HomeState {
  names: Array<[string, Map<string, number>]>;
}

export default class Home extends React.PureComponent<{}, HomeState> {
  state: HomeState;
  constructor(props) {
    super(props);
    this.state = {
      names: new Array()
    };
  }
  onGenerate = (name: string, weights: Map<string, number>) => {
    const names = Array.from(this.state.names);
    names.unshift([name, weights]);
    this.setState({
      names
    });
  };
  render() {
    return (
      <>
        <Generator onGenerate={this.onGenerate} />
        {this.state.names.length > 0 && <Names names={this.state.names} />}
      </>
    );
  }
}
