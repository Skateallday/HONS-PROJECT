const webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


const config = {
  entry:  {
  "index" :__dirname + '/src/index.js',
  "post" :__dirname + '/src/post.js'},
  output: {
    path:__dirname +"/public/",
    filename: "[name].js",
  },
  resolve: {
      extensions: [".js", ".jsx", ".css"]
  },
  module: {
      rules: [
          {
              test: /\.jsx?/,
              exclude: /node_modules/,
              use: 'babel-loader'
          },
          {
              test: /\.css$/,
              use: ExtractTextPlugin.extract({
                  fallback: 'style-loader',
                  use: 'css-loader',
              })
          },
          {
              test: /\.(png|svg|jpg|gif)$/,
              loader: "file-loader?name=[name].[ext]"
            }
      ]
  },
  plugins: [
      new ExtractTextPlugin('styles.css'),
  ]
};

module.exports = config;