<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :rules="loginRules"
      :model="loginForm"
      class="login-form"
      auto-complete="on">
      <h1 class="title">西大校园网</h1>
      <el-form-item prop="account">
        <el-select
          size="large"
          placeholder="请选择身份"
          prefix="el-icon-s-custom"
          v-model="loginForm.role">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <el-input
          size="large"
          placeholder="账号"
          prefix-icon="el-icon-s-custom"
          v-model="loginForm.userName">
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          size="large"
          placeholder="密码"
          type="password"
          prefix-icon="el-icon-lock"
          v-model="loginForm.password"
          @keyup.enter.native="handleLogin">
        </el-input>
      </el-form-item>
      <el-button :loading="loading" type="primary" size="large" class="login-btn" @click.native.prevent="handleLogin">
        登录
      </el-button>
    </el-form>
  </div>
</template>

<script>

  export default {
    name: 'login',
    data () {
      return {
        loginForm: {
          userName: '',
          password: '',
          role: ''
        },
        loginRules: {
          userName: [
            { required: true, message: '账号不能为空', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '密码不能为空', trigger: 'blur' }
          ],
          role: [
            { required: true, message: '身份不能为空', trigger: 'blur' }
          ]
        },
        loading: false,
        showDialog: false,
        options: [{
          value: 'STUDENT',
          label: '学生'
        }, {
          value: 'TEACHER',
          label: '教师'
        }]
      }
    },
    methods: {
      handleLogin () {
        this.$refs.loginForm.validate(validate => {
          if (validate) {
            this.loading = true
            this.$store.dispatch('login', this.loginForm).then(() => {
              if (this.loginForm.role == 'STUDENT') {
                this.$router.push('/project/user/student')
                this.loading = false
              } else if (this.loginForm.role == 'TEACHER') {
                this.$router.push('/project/user/teacher')
                this.loading = false
              }
            }, () => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      }
    },
    mounted () {
    }
  }
</script>

<style lang="scss">
  /*重置element*/
  $bg: #283443;
  $light_gray: #fff;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
      color: $cursor;
    }
  }

  .login-container {
    .el-input {
      input {
        background: transparent;
        border: none;

        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }

    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>

<style lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;
  .login-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;

    .login-form {
      position: relative;
      width: 520px;
      max-width: 100%;
      padding: 160px 35px 0;
      margin: 0 auto;
      overflow: hidden;

      .title {
        margin-bottom: 30px;
        text-align: center;
        color: #fff;
      }

      .login-btn {
        width: 100%;
      }
    }
  }
</style>
