<template>
  <div class="task-page">
    <div class="search-wrapper">
      <el-form v-model="searchForm" :inline="true">
        <el-form-item label="任务名称">
          <el-input v-model="searchForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker
            v-model="searchForm.taskTimeBegin"
            type="date"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="searchForm.taskTimeEnd"
            type="date"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="任务地点">
          <el-input v-model="searchForm.place" placeholder="请输入任务地点"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="operate-wrapper">
      <el-button type="primary" @click="showAdd()">新增</el-button>
      <el-button type="primary" @click="showEdit()">编辑</el-button>
      <el-button type="danger" @click="handleDelete()">删除</el-button>
    </div>
    <div class="table-wrapper">
      <template>
        <el-table
          ref="multipleTable"
          :data="tableData"
          :border=true
          @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" align="center"></el-table-column>
          <el-table-column label="序号" type="index" :index="indexMethod" width="100" align="center"></el-table-column>
          <el-table-column label="任务名称" prop="name" align="center"></el-table-column>
          <el-table-column label="任务时间" align="center">
            <template slot-scope="scope">
              {{formatDate(scope.row.beginTime)}} 至 {{formatDate(scope.row.endTime)}}
            </template>
          </el-table-column>
          <el-table-column label="任务地点" prop="place" align="center"></el-table-column>
          <el-table-column label="任务备注" prop="description" align="center"></el-table-column>
          <el-table-column label="操作" width="250" align="center">
            <template slot-scope="scope">
              <router-link
                v-for="(route, index) in routes"
                :key="index"
                :to="processLink(scope.row.id, route.path)" class="link">
                <el-button type="primary" size="mini" style="width: 128px">{{route.content}}</el-button>
              </router-link>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </div>
    <div class="page-wrapper">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="searchForm.pageIndex"
        :total=totalNumbers
        @current-change="handleCurrentChange">
      </el-pagination>
    </div>
    <div class="dialog-wrapper">
      <el-dialog
        width="600px"
        :title="dialogTitle"
        :visible.sync="showDialog"
        :close-on-click-modal=false
        @closed="dialogClosed">
        <el-form :model="formData" label-width="100px">
          <el-form-item label="任务名称">
            <el-input placeholder="请输入任务名称" v-model="formData.name"></el-input>
          </el-form-item>
          <el-form-item label="任务地点">
            <el-input placeholder="请输入任务地点" v-model="formData.place"></el-input>
          </el-form-item>
          <el-form-item label="开始时间">
            <el-date-picker
              v-model="formData.beginTime"
              type="datetime"
              placeholder="请选择开始时间"></el-date-picker>
          </el-form-item>
          <el-form-item label="结束时间">
            <el-date-picker
              v-model="formData.endTime"
              type="datetime"
              placeholder="请选择开始时间"></el-date-picker>
          </el-form-item>
          <el-form-item label="任务备注">
            <el-input placeholder="请输入任务备注" v-model="formData.remark"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="save">保存</el-button>
            <el-button @click="toggleDialog">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import { dataMixin } from '@/common/js/mixin'
  import routes from './js/routes'
  import { getPatrolTasks, getPatrolTask, addPatrolTask, editPatrolTask, deletePatrolTasks } from 'api/patrol'
  import { emptyToNull } from '@/common/js/utils/form'
  import { dateFtt } from '@/common/js/utils'

  export default {
    name: 'task-data',
    mixins: [dataMixin],
    props: {
      pageType: {
        type: String,
        default: 'patrol'
      }
    },
    data () {
      return {
        searchForm: {
          name: '',
          taskTimeBegin: '',
          taskTimeEnd: '',
          place: '',
          pageIndex: 1
        },
        formData: {
          name: '',
          place: '',
          beginTime: '',
          endTime: '',
          description: ''
        }
      }
    },
    created () {
      this.getPageData()
    },
    methods: {
      processLink (id, link) {
        const projectId = this.$route.params.projectId
        return link.replace('$id', projectId) + `?taskId=${id}`
      },
      // 显示新增页面
      showAdd () {
        this.dialogTitle = '任务新增'
        this.toggleDialog()
      },
      // 显示编辑页面
      showEdit () {
        if (this.multipleSelection.length !== 1) {
          this.$message.error('请选择一个任务进行编辑')
          return
        }
        getPatrolTask(this.multipleSelection[0]).then(res => {
          const data = res.data
          if (!data.id) {
            this.$message.error('任务不存在')
          } else {
            this.formData = data
            this.dialogTitle = '任务编辑'
            this.toggleDialog()
          }
        })
      },
      // 保存新增或编辑的数据
      async save () {
        if (!this._checkForm()) {
          return
        }
        const projectId = this.$route.params.projectId
        const request = { projectId, ...this.formData }
        let res = null
        let message = ''
        if (this.formData.id) {
          // 存在id为编辑
          res = await editPatrolTask(request)
          message = '修改成功'
        } else {
          // 不存在为编辑
          res = await addPatrolTask(request)
          message = '新增成功'
        }
        if (res.success) {
          this.$message.success(message)
          this.getPageData()
          this.toggleDialog()
        }
      },
      formatDate (date) {
        return dateFtt('yyyy-MM-dd hh:mm', new Date(date))
      },
      async getPageData () {
        const res = await getPatrolTasks(emptyToNull(this.searchForm))
        this.tableData = res.data.results
        this.totalNumbers = res.data.totalNumbers
      },
      async deletePageData () {
        const res = await deletePatrolTasks(this.multipleSelection)
        if (res.success) {
          this.$message.success('删除成功')
          this.getPageData()
        }
      },
      _checkForm () {
        const projectId = this.$route.params.projectId
        if (!projectId) {
          this.$message.error('项目不存在')
          return false
        }
        if (!this.formData.name) {
          this.$message.error('请输入任务名称')
          return false
        }
        if (!this.formData.place) {
          this.$message.error('请输入任务地点')
          return false
        }
        if (!this.formData.beginTime) {
          this.$message.error('请选择开始时间')
          return false
        }
        if (!this.formData.endTime) {
          this.$message.error('请选择结束时间')
          return false
        }
        return true
      }
    },
    computed: {
      routes () {
        return routes[this.pageType] || []
      }
    }
  }
</script>

<style lang="scss" scoped>
  .task-page {
    position: relative;

    .operate-wrapper {
      margin-bottom: 20px;
    }

    .table-wrapper {
      margin-bottom: 20px;

      .link {
        display: block;
        padding-bottom: 5px;

        &:last-child {
          padding-bottom: 0;
        }
      }
    }

    .page-wrapper {
      text-align: center;
      padding-top: 30px;
    }
  }
</style>
