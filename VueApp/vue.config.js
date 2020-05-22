const path = require('path')

module.exports = {
  //baseUrl: '/',
  outputDir: 'dist',
  lintOnSave: true,
  chainWebpack: (config) => {

    config.resolve.symlinks(true)

    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
      .tap(options => {
        return options
      })
  },
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      config.mode = 'production'
    } else {
      config.mode = 'development'
    }

    Object.assign(config, {
      resolve: {
        alias: {
          '@': path.resolve(__dirname, './src'),
          '@c': path.resolve(__dirname, './src/components'),
          'api': path.resolve(__dirname, './src/api')
        },
        mainFiles: ['index'],
        extensions: ['.js', '.json', '.vue']
      }
    })
  },
  productionSourceMap: true,
  // css相关配置
  css: {
    sourceMap: false,
    loaderOptions: {},
    modules: false
  },
  parallel: require('os').cpus().length > 1,
  pwa: {},
  devServer: {
    open: true,
    host: '0.0.0.0',
    port: 8080,
    https: false,
    hotOnly: false,
    before: (app) => {
    }
  },
  pluginOptions: {
    // ...
  }
}
