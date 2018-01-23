import * as React from "react";
import { ShareButtons } from "react-share";
import { Button, Icon, Input, Popup } from "semantic-ui-react";
import CopyToClipboard from "react-copy-to-clipboard";

declare var BASE_URL: string;

interface ShareProps {
  name: string;
  weights: Map<string, number>;
}

interface ShareState {
  copied: boolean;
  description: string;
  url: string;
}

export default class Share extends React.PureComponent<ShareProps, ShareState> {
  state: ShareState;
  constructor(props) {
    super(props);
    const weights = btoa(
      JSON.stringify(
        Array.from(this.props.weights)
          .filter(([_, weight]) => weight > 0)
          .map(([name, weight]) => [name, weight.toFixed(2)])
      )
    );
    this.state = {
      copied: false,
      description:
        `What fantasy series is ${this.props.name} from? The ` +
        `answer may surprise you!`,
      url: `${BASE_URL}/#/preview/${this.props.name}/${weights}`
    };
    console.log(this.state.url);
  }
  onCopy = (_, result) => {
    this.setState({
      copied: result
    });
  };
  onClose = () => {
    this.setState({
      copied: false
    });
  };
  render() {
    const clipboard = (
      <div>
        <Input action>
          <input value={this.state.url} />
          <CopyToClipboard text={this.state.url} onCopy={this.onCopy}>
            <Button
              icon={this.state.copied ? "check" : "copy"}
              color={this.state.copied ? "green" : undefined}
            />
          </CopyToClipboard>
        </Input>
      </div>
    );
    return (
      <>
        <Button.Group basic>
          <ShareButtons.TwitterShareButton
            url={this.state.url}
            title={this.state.description}
          >
            <Button icon="twitter" color="blue" />
          </ShareButtons.TwitterShareButton>
          <ShareButtons.FacebookShareButton
            url={this.state.url}
            quote={this.state.description}
          >
            <Button icon="facebook" color="facebook" />
          </ShareButtons.FacebookShareButton>
          <ShareButtons.TumblrShareButton
            url={this.state.url}
            title={this.state.description}
          >
            <Button icon="tumblr" color="blue" />
          </ShareButtons.TumblrShareButton>
          <Popup
            content={clipboard}
            on="click"
            onClose={this.onClose}
            trigger={
              <Button icon>
                <Icon name="linkify" />
              </Button>
            }
          />
        </Button.Group>
      </>
    );
  }
}
