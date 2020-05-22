import { baseInstance } from './request'

export function login ({ userName, password, role }) {
  return baseInstance({
    url: '/admin/login/user',
    data: {
      userName,
      password,
      role
    }
  })
}
