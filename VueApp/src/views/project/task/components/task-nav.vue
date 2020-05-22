<template>
  <div class="task-nav">
    <router-link v-for="(item, index) in routes" :key="index" :to="replacePath(item.path)" class="link">
      <el-button :type="buttonType(item.component)">{{item.content}}</el-button>
    </router-link>
  </div>
</template>

<script>
  export default {
    name: 'task-nav',
    props: {
      routes: {
        type: Array,
        default () {
          return []
        }
      }
    },
    methods: {
      replacePath (path) {
        const taskId = this.$route.query.taskId
        return path.replace('$id', this.$route.params.projectId) + '?taskId=' + taskId
      },
      buttonType (component) {
        const routeComponent = this.$route.meta.component
        return routeComponent && routeComponent === component ? 'primary' : 'default'
      }
    }
  }
</script>

<style lang="scss" scoped>
  .task-nav {
    .link {
      margin-right: 20px;
      &:last-child {
        margin-right: 0;
      }
    }
  }
</style>
