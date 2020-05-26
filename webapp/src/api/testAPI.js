import { baseInstance } from './request'


export function testCountQuery ({ db_views }) {
  return baseInstance({
    url: '/server/test/count/query',
    method: 'post',
    data: {
      db_views
    }
  })
}
