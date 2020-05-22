<template>
  <div class="app-main">
    <router-view />
  </div>
</template>

<script>
  export default {
    name: 'appMain'
  }
</script>

<style lang="scss" scoped>
  .app-main {
    position: absolute;
    top: 60px;
    bottom: 0;
    width: 100%;
    box-sizing: border-box;
    .breadcrumb-wrapper {
      padding: 10px 20px;
      box-shadow: 0 1px 4px rgba(0, 21, 41, .08);
      font-size: 20px;
    }
  }
</style>
