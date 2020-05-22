import * as types from './mutation-types'

const mutations = {
  [types.SET_LOGIN] (state, flag) {
    state.isLogin = flag
  },
  [types.SET_USER_NAME] (state, userName) {
    state.userName = userName
  },
  [types.SET_IS_SUPER] (state, isSuper) {
    state.isSuper = isSuper
  },
  [types.SET_USER_ID] (state, userId) {
    state.userId = userId
  }
}

export default mutations
