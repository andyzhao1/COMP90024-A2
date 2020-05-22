<template>
  <div class="assets-page">
    <div class="search-wrapper">
      <el-form :model="searchForm" :inline=true>
        <slot name="search"></slot>
        <el-form-item>
          <el-button @click="handleSearch" type="primary">搜索</el-button>
          <el-button @click="handleCancelSearch">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="table-wrapper">
      <slot name="table">
      </slot>
    </div>
    <pagination :total="total" :current-page="currentPage" @current-change="currentChange"></pagination>
  </div>
</template>

<script>
  import Pagination from '@c/pagination/pagination'

  export default {
    name: 'assets-page',
    props: {
      total: {
        type: Number,
        default: 0
      },
      searchForm: {
        type: Object,
        default: null
      },
      currentPage: {
        type: Number,
        default: 1
      },
      canAdd: {
        type: Boolean,
        default: true
      },
      canDelete: {
        type: Boolean,
        default: true
      }
    },
    methods: {
      currentChange (currentPage) {
        this.$emit('current-change', currentPage)
      },
      handleAdd () {
        this.$emit('data-add')
      },
      handleDelete () {
        this.$emit('data-delete')
      },
      handleSearch () {
        this.$emit('data-search')
      },
      handleCancelSearch () {
        this.$emit('data-cancel')
      }
    },
    components: {
      Pagination
    }
  }
</script>

<style lang="scss" scoped>
  .assets-page {
    padding-top: 30px;
    .table-wrapper {
      margin-top: 30px;
    }
  }
</style>
