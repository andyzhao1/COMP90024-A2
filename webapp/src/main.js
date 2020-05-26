import Vue from 'vue'

import App from './App.vue'
import router from './router'

import './plugins/element.js'
import './common/scss/index.scss'
import './permission'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/pie'
import 'echarts/lib/chart/line'
import 'echarts/lib/component/title'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/legend/ScrollableLegendModel.js'
import 'echarts/lib/component/legend/ScrollableLegendView.js'
import 'echarts/lib/component/legend/scrollableLegendAction.js'

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
  render: h => h(App)
}).$mount('#app')
Vue.component('v-chart', ECharts)
