const path = require("path");
const merge = require("webpack-merge");
const webpack = require("webpack");
const baseConfig = require("./webpack.config.js");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");

module.exports = merge(baseConfig, {
  devtool: "",
  plugins: [
    new CopyWebpackPlugin([
      {
        from: path.join(__dirname, "src", "vars"),
        to: "vars/"
      },
      { from: path.join(__dirname, "src", "index.html") }
    ]),
    new UglifyJsPlugin(),
    new webpack.DefinePlugin({
      BASE_URL: "https://crestonbunch.github.io/neural-namer-demo"
    })
  ]
});
