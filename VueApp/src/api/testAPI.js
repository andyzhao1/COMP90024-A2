import { baseInstance } from './request'

// 查询学生
export function testCountQuery ({ db_views }) {
  return baseInstance({
    url: '/server/test/count/query',
    method: 'post',
    data: {
      db_views
    }
  })
}
