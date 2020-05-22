/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import scenarioRouter from './module/scenario'
import mapRouter from './module/map'
import harvesterRouter from './module/harvester'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  mode: 'hash',
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login')
    },
    scenarioRouter,
    mapRouter,
    harvesterRouter
  ]
})

router.beforeEach((to, from, next) => {
  // 添加百度统计
  if (to.path) {
    _hmt.push(['_trackPageview', to.fullPath])
  }

  const isLogin = store.getters.isLogin
  if (!isLogin) {
    if (to.path === '/') {
      next('/overview/scenario')
    } else {
      next()
    }
  } else {
    if (to.path === '/login') {
      next('/project/user/data')
    } else {
      next('/login')
    }
  }
})

export default router
