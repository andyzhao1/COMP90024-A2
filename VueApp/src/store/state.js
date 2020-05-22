let userInfo = sessionStorage.getItem('User_Info')

userInfo = userInfo ? JSON.parse(userInfo) : {}

const state = {
  isLogin: userInfo.isLogin || false,
  userName: userInfo.userName || '',
  isSuper: userInfo.isSuper || false,
  userId: userInfo.userId || ''
}

export default state
