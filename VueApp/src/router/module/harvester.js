import Layout from '@/layout/index.vue'

const harvesterRouter = {
  path: '/harvester',
  name: 'harvester',
  meta: {
    title: 'Harvester'
  },
  component: Layout,
  children: [
    {
      path: 'search',
      name: 'search',
      meta: {
        title: 'search'
      },
      component: () => import('@/views/harvester/search')
    }
  ]
}
export default harvesterRouter
