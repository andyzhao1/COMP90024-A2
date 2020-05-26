<template>
  <div class="side-bar">
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :background-color="variable.menuBg"
        :text-color="variable.menuText"
        :unique-opened="false"
        :active-text-color="variable.menuActiveText"
        :collapse-transition="false"
        :router=true
        :default-active="$route.path"
        mode="vertical">
        <el-submenu index="1" >
          <template slot="title">
            <i class="el-icon-s-promotion"></i>
            <span>Overview</span>
          </template>
          <el-menu-item index="/overview/scenario">Scenario</el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-s-promotion"></i>
            <span>Map</span>
          </template>
          <el-menu-item index="/map/melbourne">Melbourne</el-menu-item>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">
            <i class="el-icon-s-promotion"></i>
            <span>Harvester</span>
          </template>
          <el-menu-item index="/harvester/search">Search Tweets</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-scrollbar>
  </div>
</template>
<script>
  import variable from '@/common/scss/variable.scss'
  import { mapGetters } from 'vuex'
  export default {
    name: 'sideBar',
    created () {
      this.role = ""
    },
    data () {
      return {
        role: ''
      }
    },
    computed: {
      variable () {
        return variable
      },
      ...mapGetters([
        'role'
      ])
    }
  }
</script>

<style lang="scss">
  .side-bar {
    height: 100%;
  }
</style>
