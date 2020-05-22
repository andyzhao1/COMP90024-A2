import { baseInstance } from './request'
// queryCollectingThreadList
export function queryCollectingThreadList () {
    return baseInstance({
      url: '/harvester/search/queryCollectingThreadList',
      method: 'get',
      data: {
      }
    })
}

// startCollectByRadius
export function startCollectByRadius ({db_name, provinces, geocodes, since, until, query }) {
  return baseInstance({
    url: '/harvester/search/startCollectByRadius',
    method: 'post',
    data: {
      db_name,
      provinces,
      geocodes,
      since,
      until,
      query
    }
  })
}

// stopCollectByRadius
export function stopCollectByRadius (ids) {
  return baseInstance({
    url: '/harvester/search/stopCollectByRadius',
    method: 'post',
    data: {
      ids
    }
  })
}
