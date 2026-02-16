const path = require('path')
module.exports = {
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',
  productionSourceMap: false,
  devServer: {
    hot: true,
    port: 8010,
    open: true,
    proxy: {
      '/': {
        target: 'http://192.168.5.133:8888/',
        changeOrigin: true,
        pathRewrite: { '^/': '' },
      },
    },
  },
  configureWebpack: {
    name: 'system',
    resolve: {
      alias: {
        "~@": __dirname,
        "@": path.resolve(__dirname, "./src")
      }
    }
  },
}
