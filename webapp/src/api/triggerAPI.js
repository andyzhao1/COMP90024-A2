import { baseInstance } from './request'
// queryCollectingThreadList
export function queryTask () {
    return baseInstance({
      url: '/trigger/tasks/query',
      method: 'get',
      data: {
      }
    })
}

// startCollectByRadius
export function addTask ({db_names, provinces, geocodes, query }) {
  return baseInstance({
    url: '/trigger/tasks/add',
    method: 'post',
    data: {
      db_names,
      provinces,
      geocodes,
      query
    }
  })
}

// stopCollectByRadius
export function deleteTask (ids) {
  return baseInstance({
    url: '/trigger/tasks/delete',
    method: 'post',
    data: {
      ids
    }
  })
}
