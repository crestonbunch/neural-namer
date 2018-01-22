const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");

module.exports = {
  context: path.resolve(__dirname),
  entry: "./src/index.tsx",
  devtool: "inline-source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"]
  },
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist")
  },
  devServer: {
    contentBase: path.resolve(__dirname, "src"),
    compress: true,
    hot: true,
    inline: true
  },
  plugins: [
    new CopyWebpackPlugin([
      {
        from: path.join(__dirname, "src", "vars"),
        to: "vars/"
      },
      { from: path.join(__dirname, "src", "index.html") }
    ]),
    new webpack.HotModuleReplacementPlugin()
  ],
  watch: true
};
