var path = require("path");
var webpack = require("webpack");
var ExtractTextPlugin = require("extract-text-webpack-plugin");


module.exports = {
    devtool: "cheap-module-eval-source-map",
    entry: {
        app: "./src/index",
        vendor: [
            "classnames", "history", "immutable", "lodash", "moment",
            "nprogress", "react", "react-bootstrap", "react-dom", "react-redux",
            "react-router", "redux", "redux-logger", "redux-thunk",
            "reselect", "superagent"
        ],
    },
    resolve: {
        modulesDirectories: ["src", "node_modules"]
    },
    output: {
        path: path.join(__dirname, "build"),
        filename: "js/bundle.js",
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin("vendor", "js/vendor.bundle.js"),
        new ExtractTextPlugin("stylesheets.css"),
        new webpack.NoErrorsPlugin()
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loaders: ["babel"],
                include: path.join(__dirname, "src")
            },
            {
                // expose immutable globally so we can use it in app.html
                test: require.resolve("immutable"),
                loader: "expose?immutable"
            },
            {
                test: /\.less$/,
                loader: ExtractTextPlugin.extract("css?sourceMap!less?sourceMap")
            },
            {
                // move font files found within CSS to the build directory
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file?name=[path][name].[ext]?[hash]&context=./node_modules"
            },
            {
                // move images found within CSS to the build directory
                test: /\.(jpg|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file?name=[path][name].[ext]?[hash]&context=./node_modules"
            },
            { 
                test: /(\.css$)/, 
                loaders: ['style-loader', 'css-loader', 'postcss-loader'] 
            }
        ]
    }
};
