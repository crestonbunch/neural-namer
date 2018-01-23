import * as React from "react";
import * as ReactDOM from "react-dom";
import { Route, Switch } from "react-router";
import { HashRouter, Link } from "react-router-dom";
import { Container, Menu, Icon } from "semantic-ui-react";

import About from "./components/container/About";
import Home from "./components/container/Home";
import Preview from "./components/container/Preview";

const root = (
  <HashRouter>
    <Container text>
      <Menu secondary>
        <Link to="/">
          <Menu.Item header fitted="horizontally">
            Neural Namer
          </Menu.Item>
        </Link>
        <Menu.Menu position="right">
          <a href="https://github.com/crestonbunch/neural-namer">
            <Menu.Item>
              <Icon name="github" size="big" />
            </Menu.Item>
          </a>
          <Link to="/about">
            <Menu.Item position="right">
              <Icon name="help" size="big" />
            </Menu.Item>
          </Link>
        </Menu.Menu>
      </Menu>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/preview/:name/:weights" component={Preview} />
      </Switch>
    </Container>
  </HashRouter>
);

ReactDOM.render(root, document.getElementById("root"));
