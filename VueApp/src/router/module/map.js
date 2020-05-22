import Layout from '@/layout/index.vue'

const mapRouter = {
  path: '/map',
  name: 'melbourne.vue',
  meta: {
    title: 'Map'
  },
  component: Layout,
  children: [
    {
      path: 'melbourne',
      name: 'melbourne',
      meta: {
        title: 'Melbourne'
      },
      component: () => import('@/views/map/melbourne')
    }
  ]
}
export default mapRouter
