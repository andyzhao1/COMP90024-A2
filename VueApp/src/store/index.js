import Vue from 'vue'
import Vuex from 'vuex'
import state from './state'
import mutations from './mutaions'
import actions from './actions'
import * as getters from './getters'
import createLogger from 'vuex/dist/logger'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
export default new Vuex.Store({
  state,
  mutations,
  actions,
  getters,
  plugins: debug ? [createLogger()] : []
})
