<template>
  <div class="search">
    <assets-page
      :total="totalNumbers"
      :search-form="searchForm"
      :currentPage="searchForm.pageIndex"
      @current-change="handleCurrentChange"
      @data-add="showAdd"
      @data-cancel="handleCancel"
      @data-delete="handleDelete"
      @data-search="handleSearch">
      <el-form-item label="Thread ID" slot="search">
        <el-input v-model="searchForm.departmentName" placeholder="Thread ID"></el-input>
      </el-form-item>
      <div slot="table">
        <el-table
          ref="multipleTable"
          :data="tableData"
          style="width: 100%"
          :border=true
          @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" align="center"></el-table-column>
          <el-table-column label="index" type="index" :index="indexMethod" width="55" align="center"></el-table-column>
          <el-table-column label="id" prop="id" align="center"></el-table-column>
          <el-table-column label="province" prop="information.provinces[0]" align="center"></el-table-column>
          <el-table-column label="geocode" prop="information.geocodes[0]" align="center"></el-table-column>
          <el-table-column label="since" prop="information.since" align="center"></el-table-column>
          <el-table-column label="until" prop="information.until" align="center"></el-table-column>
          <el-table-column label="query" prop="information.query" align="center"></el-table-column>
        </el-table>
      </div>
    </assets-page>
    <div class="dialog-wrapper">
      <el-dialog
        :title="dialogTitle"
        :visible.sync="showDialog"
        :close-on-click-modal=false
        width="600px"
        @closed="dialogClosed">
        <el-form :model="formData" label-width="100px">
          <el-form-item label="Province">
            <el-input placeholder="Input province" v-model="formData.provinces"></el-input>
          </el-form-item>
          <el-form-item label="geocode">
            <el-input placeholder="Input geocode" v-model="formData.geocodes"></el-input>
          </el-form-item>
          <el-form-item label="since">
            <el-input placeholder="Input since" v-model="formData.since"></el-input>
          </el-form-item>
          <el-form-item label="until">
            <el-input placeholder="Input until" v-model="formData.until"></el-input>
          </el-form-item>
          <el-form-item label="db name">
            <el-input placeholder="Input database name" v-model="formData.db_name"></el-input>
          </el-form-item>
          <el-form-item label="query">
            <el-input placeholder="Input query" v-model="formData.query"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="save">Save</el-button>
            <el-button @click="toggleDialog">Cancel</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>

  </div>
</template>

<script>
  import { dataMixin } from '@/common/js/mixin'
  import routes from '@/common/js/config/routes'
  import AssetsPage from '@/components/assets-page'
  import { queryCollectingThreadList,startCollectByRadius,stopCollectByRadius } from 'api/collectTwitterAPI'

  export default {
    name: 'traffic',
    mixins: [dataMixin],
    data () {
      return {
        searchForm: {
          departmentName: '',
          pageIndex: 1
        },
        formData: {
          provinces: null,
          geocodes: null,
          since: null,
          until: null,
          query: null
        }
      }
    },
    created () {
      this.getPageData()
    },
    methods: {
      showAdd () {
        this.dialogTitle = 'Add'
        this.toggleDialog()
      },
      showEdit (data) {
        this.dialogTitle = 'Edit'
        this.setFormData(data)
        this.toggleDialog()
      },
      async save () {
        if (!this._checkForm()) {
          return
        }
        let message = ''
        let res = null
        if (this.formData.id) {
        } else {
          this.formData.provinces = [this.formData.provinces]
          this.formData.geocodes = [this.formData.geocodes]
          if (this.formData.query != null) {
            this.formData.query = [this.formData.query]
          }
          this.formData.db_name = [this.formData.db_name]
          res = await startCollectByRadius(this.formData)
          message = 'Add successfully'
        }
        if (res.isSuccess) {
          this.$message.success(message)
          this.getPageData()
          this.toggleDialog()
        } else {
        }
      },
      async getPageData () {
        const res = await queryCollectingThreadList()
        if (res.isSuccess) {
          this.tableData = res.threadList
          this.tableData.forEach(item => {
            item['id'] = item['thread_id']
          })
          console.log(this.tableData)
        } else {
          this.getPageData()
        }
      },
      async deletePageData () {
        console.log(this.multipleSelection)
        const res = await stopCollectByRadius(this.multipleSelection)
        if (res.isSuccess) {
          this.$message.success('删除成功')
          this.getPageData()
        } else {
          this.deletePageData()
        }
      },
      _checkForm () {
        return true
      }
    },
    components: {
      AssetsPage
    },
    computed: {
      routes () {
        return routes.student
      }
    }
  }
</script>

<style lang="scss" scoped>
  .search {
    padding: 20px;

    .device-icon {
      font-size: 28px;
    }
  }
</style>
