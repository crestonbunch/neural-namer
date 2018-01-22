import * as React from "react";
import { Label, Segment } from "semantic-ui-react";

interface NameProps {
  names: Array<[string, Map<string, number>]>;
}

export default class Names extends React.PureComponent<NameProps, {}> {
  constructor(props) {
    super(props);
  }
  render() {
    return this.props.names.map(([name, weights]) => {
      return (
        <React.Fragment key={name}>
          <Segment attached="top" color="black" size="huge">
            {name}
          </Segment>
          <Segment attached="bottom" size="tiny">
            <Label.Group>
              {Array.from(weights).map(
                ([author, weight]) =>
                  weight > 0 ? (
                    <Label>
                      {author}
                      <Label.Detail>
                        {`${(weight * 100).toFixed(0)}%`}
                      </Label.Detail>
                    </Label>
                  ) : null
              )}
            </Label.Group>
          </Segment>
        </React.Fragment>
      );
    });
  }
}
