const merge = require("webpack-merge");
const baseConfig = require("./webpack.config.js");

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
    new UglifyJsPlugin({
      sourceMap: true
    }),
    new CopyWebpackPlugin.DefinePlugin({
      "process.env.NODE_ENV": "production"
    })
  ]
});
