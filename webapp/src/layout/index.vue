<template>
  <div class="layout">
    <div class="sidebar-container">
      <side-bar></side-bar>
    </div>
    <div class="main-container">
      <div class="header">
        <nav-bar></nav-bar>
      </div>
      <app-main></app-main>
    </div>
  </div>
</template>

<script>
  import { AppMain, NavBar, SideBar } from './components'

  export default {
    name: 'layout',
    components: {
      AppMain,
      NavBar,
      SideBar
    }
  }
</script>

<style lang="scss" scoped>
  @import "~@/common/scss/mixin";
  @import "~@/common/scss/variable";

  .layout {
    @include clearfix;
    position: relative;
    width: 100%;
    height: 100%;
    .main-container {
      box-sizing: border-box;
      height: 100%;
    }
  }
</style>
