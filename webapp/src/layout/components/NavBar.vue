<template>
  <div class="navbar">
    <div class="breadcrumb-wrapper">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item v-for="(item, index) in levelList" :key="index">
          <span class="isBack" v-if="item.backPath" @click="goBack(item.backPath)">{{item.meta.title}}</span>
          <span v-else>{{item.meta.title}}</span>
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right-menu">
      <el-dropdown trigger="click">
        <div class="user-wrapper">
          <img class="avatar"
               src="logo.png"/>
          <span class="name">Group55</span>
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="showChange">Members</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <div class="dialog-wrapper">
        <el-dialog
          title="Members"
          :visible.sync="dialogShow"
          :close-on-click-modal=false
          @close="dialogClosed"
          width="600px">
          <el-form :model="formData" :rules="rules" ref="ruleForm" label-width="100px">
            <el-form-item label="Member 1:" style="height: 50px">
              <p>CHUANRU WAN ---- 1074738</p>
            </el-form-item>
            <el-form-item label="Member 2:" style="height: 50px">
              <p>Zhujun Hu ---- 1094242</p>
            </el-form-item>
            <el-form-item label="Member 3:" style="height: 50px">
              <p>Shengzhe Zhao ---- 1074171</p>
            </el-form-item>
            <el-form-item label="Member 4:" style="height: 50px">
              <p>Rajeong Moon ---- 972583</p>
            </el-form-item>
            <el-form-item label="Member 5:" style="height: 50px">
              <p>Sejin Kim ---- 1025560 </p>
            </el-form-item>
          </el-form>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'navBar',
    data () {
      const validatePass2 = (rule, value, callback) => {
        if (value !== this.formData.password) {
          callback(new Error('两次密码输入不一致'))
        } else {
          callback()
        }
      }
      return {
        dialogShow: false,
        levelList: [],
        formData: {
          oldPassword: '',
          password: '',
          checkPassword: ''
        },
        rules: {
          oldPassword: [
            { required: true, message: '请输入旧密码', trigger: 'blur' },
            { min: 6, max: 12, message: '长度在6 到 12个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入新密码', trigger: 'blur' },
            { min: 6, max: 12, message: '长度在6 到 12个字符', trigger: 'blur' }
          ],
          checkPassword: [
            { required: true, message: '请确认密码', trigger: 'blur' },
            { min: 6, max: 12, message: '长度在6 到 12个字符', trigger: 'blur' },
            { validator: validatePass2, trigger: 'blur' }
          ]
        }
      }
    },
    created () {
      this.getBreadcrumb()
    },
    methods: {
      handleLogout () {
        this.$store.dispatch('logout').then(() => {
          this.$router.push('/login')
        })
      },
      goBack (path) {
        this.$router.push(path)
      },
      getBreadcrumb () {
        const matched = this.$route.matched
        let levelList = matched.filter(item => item.meta && item.meta.title)
        let projectId = this.$route.params.projectId
        this.levelList = levelList.map(item => {
          if (item.meta.isBack) {
            let path = item.redirect || item.path
            item.backPath = projectId ? path.replace(':projectId', projectId) : path
          } else {
            item.backPath = ''
          }
          return item
        })
      },
      showChange () {
        this.toggleDialog()
      },
      toggleDialog () {
        this.dialogShow = !this.dialogShow
      },
      dialogClosed () {
        this.$refs.ruleForm.resetFields()
      },
      changePassword () {
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            changePassword(this.formData).then(res => {
              if (res.success) {
                this.$message.success('密码修改成功')
                this.toggleDialog()
              }
            })
          } else {
            return false
          }
        })
      }
    },
    computed: {
      ...mapGetters([
        'userName'
      ])
    },
    watch: {
      $route () {
        this.getBreadcrumb()
      }
    }
  }
</script>

<style lang="scss" scoped>
  .navbar {
    position: relative;
    display: flex;
    padding: 0 20px;
    height: 60px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, .08);
    align-items: center;
    justify-content: space-between;

    .breadcrumb-wrapper {
      .isBack {
        color: #409eff;
        cursor: pointer;
      }
    }

    .right-menu {
      cursor: pointer;

      .user-wrapper {
        display: flex;
        align-items: center;

        .avatar {
          width: 40px;
          height: 40px;
          margin-right: 10px;
          border-radius: 10px;
        }
      }
    }
  }
</style>
