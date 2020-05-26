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

// Scenario 4 unemploymentRate
export function unemploymentRate ({ sa2_main11 }) {
  return baseInstance({
    url: '/server/data/unemploymentrate',
    method: 'post',
    data: {
      sa2_main11
    }
  })
}

// Scenario 4 job related count
export function jobRelatedTweetsDistribution () {
  return baseInstance({
    url: '/server/data/jobRelatedTweetsDistribution',
    method: 'get',
    data: {
    }
  })
}

// Scenario 2 education background
export function educationBackground () {
  return baseInstance({
    url: '/server/data/educationBackground',
    method: 'get',
    data: {
    }
  })
}

// Scenario 3 industryOfEmploymentByOccupation
export function industryOfEmploymentByOccupation () {
  return baseInstance({
    url: '/server/data/industryOfEmploymentByOccupation',
    method: 'get',
    data: {
    }
  })
}

// Scenario 1 centrelink
export function centrelink () {
  return baseInstance({
    url: 'server/data/centrelink',
    method: 'get',
    data: {
    }
  })
}

// Scenario 1 socialBenifit
export function socialBenifit () {
  return baseInstance({
    url: 'server/data/socialBenifit',
    method: 'get',
    data: {
    }
  })
}
