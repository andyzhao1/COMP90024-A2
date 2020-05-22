<template>
  <div class="pagination-wrapper">
    <el-pagination
      background
      layout="prev, pager, next"
      :current-page="currentPage"
      :total="total"
      @current-change="currentChange">
    </el-pagination>
  </div>
</template>

<script>
  export default {
    name: 'pagination',
    props: {
      total: {
        type: Number,
        default: 0
      },
      currentPage: {
        type: Number,
        default: 1
      }
    },
    methods: {
      currentChange (currentPage) {
        this.$emit('current-change', currentPage)
      }
    }
  }
</script>

<style lang="scss" scoped>
  .pagination-wrapper {
    position: relative;
    width: 100%;
    padding-top: 30px;
    text-align: center;
  }
</style>
