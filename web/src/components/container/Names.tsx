import * as React from "react";
import { Grid, Label, Segment } from "semantic-ui-react";

import Share from "./Share";

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
            <Grid>
              <Grid.Row columns={2}>
                <Grid.Column>{name}</Grid.Column>
                <Grid.Column textAlign="right">
                  <Share name={name} weights={weights} />
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Segment>
          <Segment attached="bottom" size="tiny">
            <Label.Group>
              {Array.from(weights).map(
                ([author, weight]) =>
                  weight > 0 ? (
                    <Label key={author}>
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
