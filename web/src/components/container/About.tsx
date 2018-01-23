import * as React from "react";
import { Header } from "semantic-ui-react";

export default class About extends React.PureComponent<{}, {}> {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <>
        <Header dividing>What is this?</Header>
        <p>
          Neural Namer is a{" "}
          <a href="https://karpathy.github.io/2015/05/21/rnn-effectiveness/">
            recurrent neural network (RNN)
          </a>{" "}
          trained on fantasy names that runs{" "}
          <a href="https://deeplearnjs.org/">entirely in your browser</a>. The
          archictecture of neural namer allows it to build names in the style of
          specific authors. During training it learns{" "}
          <a href="https://en.wikipedia.org/wiki/Word_embedding">vectors</a>{" "}
          that encode information about each author's naming style. During
          inference (i.e., when you hit the big green button) it uses these
          vectors to generate names that the same author might come up with!
        </p>
        <p>
          By combining these vectors using the sliders, the network can
          hallucinate entirely new authors! Roughly speaking it tries to answer
          the question: "what names would Tolkien and George R. R. Martin come
          up with if they mind melded?"
        </p>
        <Header dividing>What about author (x)?</Header>
        <p>
          The more data the merrier! If you know of a prolific fantasy author
          and would like to add it to the dataset, I accept pull requests{" "}
          <a href="https://github.com/crestonbunch/neural-namer">on Github</a>.
          The entire project is open source!
        </p>
        <p>
          If you're specifically asking about <b>Brandon Sanderson</b>, then
          please tell the fine admins over at the{" "}
          <a href="http://stormlightarchive.wikia.com/">
            Stormlight Archive Wikia
          </a>{" "}
          to make a{" "}
          <a href="http://stormlightarchive.wikia.com/wiki/Special%3AStatistics">
            data dump
          </a>{" "}
          available to download.
        </p>
        <Header dividing>Why are some names actual character names?</Header>
        <p>
          That's just the nature of neural networks, a small dataset, and the{" "}
          <a href="https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff">
            bias-variance tradeoff
          </a>.
        </p>
        <p>
          Making the network smaller means you'll see fewer actual names, but
          the names will be less similar to the author's style. On the other
          hand, making it too big means it will just learn to generate exact
          names from the dataset and never try to come up with any on its own.
        </p>
      </>
    );
  }
}
