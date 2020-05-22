import { baseInstance } from './request'

// Scenario 1
export function queryScenario ({ scenario }) {
  return baseInstance({
    url: '/server/scenario/query',
    method: 'post',
    data: {
      scenario
    }
  })
}
