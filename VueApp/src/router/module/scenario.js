import Layout from '@/layout/index.vue'

const scenarioRouter = {
  path: '/overview',
  name: 'overview',
  meta: {
    title: 'Overview'
  },
  component: Layout,
  children: [
    {
      path: 'scenario',
      name: 'scenario',
      meta: {
        title: 'Scenario'
      },
      component: () => import('@/views/scenario/scenario')
    }
  ]
}
export default scenarioRouter
