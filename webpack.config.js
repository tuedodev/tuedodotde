const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
	resolve: {
		modules: ['node_modules'],
	},
	entry: ['@babel/polyfill', './src/static/js/index.js'],
	output: {
		path: path.resolve(__dirname, 'src/static/dist'),
		publicPath: '/static/',
		filename: 'bundle.js',
	},
	optimization: {
		minimize: true,
	},
	module: {
		rules: [
			{
				test: /\.scss$/,
				use: [
					{
						loader: MiniCssExtractPlugin.loader,
						options: {},
					},
					{
						loader: 'css-loader',
					},
					{
						loader: 'sass-loader',
						options: {
							sourceMap: true,
						},
					},
				],
			},
			{
				test: /\.css$/i,
				use: ['style-loader', 'css-loader'],
			},
			{
				test: /\.(png|svg|jpe?g|gif)$/,
				use: [
					{
						loader: 'file-loader',
						options: {
							name: '[name].[ext]',
							outputPath: 'img',
						},
					},
				],
			},
			{
				test: /\.js?$/,
				exclude: /node_modules/,
				loader: 'babel-loader',
				query: {
					presets: ['@babel/preset-env', { plugins: ['@babel/plugin-proposal-class-properties'] }],
				},
			},
		],
	},
	plugins: [
		new CleanWebpackPlugin(),
		new MiniCssExtractPlugin({
			filename: 'main.css',
		}),
		new CopyPlugin({
			patterns: [
				{ from: './src/static/img', to: 'img' },
				{ from: './src/static/fonts', to: 'fonts' },
			],
		}),
	],
};
