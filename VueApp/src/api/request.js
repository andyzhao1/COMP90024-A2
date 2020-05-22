import axios from 'axios'
import { Message } from 'element-ui'
import { API_HOST } from '@/common/js/config/host'

axios.defaults.retry = 4
axios.defaults.retryDelay = 5000

const baseInstance = axios.create({
  baseURL: API_HOST,
  timeout: 5000,
  method: 'post'
})

baseInstance.interceptors.request.use(config => {
  return config
}, error => {
  console.log(error)
  Message.error('网络异常A，请稍后') // 服务器异常
  return Promise.reject(error)
})

baseInstance.interceptors.response.use(response => {
  const res = response.data
  if (res.isSuccess) {
    return res
  } else {
    Message.error(res.message || '网络异常B，请稍后') // 服务器异常
    return false
  }
}, error => {
  console.log(error)
  Message.error('网络异常C，请稍后') // 服务器异常

  var config = error.config
  var backoff = new Promise(function (resolve) {
    setTimeout(function () {
      resolve()
    }, config.retryDelay || 1)
  })
  return backoff.then(function () {
    return axios(config)
  })
  // return Promise.reject(error)
})

export { baseInstance }
