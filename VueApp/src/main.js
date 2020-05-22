import Vue from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import Blob from './excel/Blob.js'
import Export2Excel from './excel/Export2Excel.js'

import './plugins/element.js'
import './common/scss/index.scss'
import './permission'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/pie'
import * as VueGoogleMaps from 'vue2-google-maps'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)

Vue.component('chart', ECharts)

Vue.use(VueGoogleMaps, {
  load: {
    apiKey: 'AIzaSyBS2bLtq4w5ofYWQ7TD6Rvm3cbpMYMa1QU',
    libraries: ['places'],
    useBetaRenderer: false
  }
})

Vue.config.productionTip = false

new Vue({
  router,
  store,
  Blob,
  Export2Excel,
  render: h => h(App)
}).$mount('#app')
Vue.component('v-chart', ECharts)
