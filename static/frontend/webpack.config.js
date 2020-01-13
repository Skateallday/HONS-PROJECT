const webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

const config = {
    entry:  {
        "index" :__dirname + '/js/index.jsx',
        "navigation" :__dirname + '/js/navigation.jsx',
        "test" : __dirname +'/js/second.jsx',
        "writing" : __dirname +'/js/writing.jsx',
        "dashboard" : __dirname +'/js/dashboard.jsx'

    },
    output: {
        path:__dirname +"/dist/",
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
                use: 'file-loader'
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('styles.css'),
    ]
}

module.exports = config;
