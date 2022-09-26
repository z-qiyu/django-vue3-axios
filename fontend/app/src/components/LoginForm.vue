<template>
  <div>
    <el-form
      label-position="left"
      label-width="100px"
      :model="form"
      style="max-width: 460px"
      :rules="rules"
      ref="form"
    >
      <el-form-item label="用户名" prop="username" required>
        <el-input v-model="form.username" type="text" />
      </el-form-item>
      <el-form-item label="密码" prop="password"  required>
        <el-input v-model="form.password" type="password" />
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="formSubmit">登录</el-button>
  </div>
</template>

<script>

import {apiLogin} from "@/apis/user";
import {ElMessage} from "element-plus";

export default {
  name: "LoginForm",
  data(){
    return {
      form:{
        username:"",
        password:""
      },
      rules:{
        username:[
            { required: true, message: '请填写用户名', trigger: 'change' },
            { min: 0, max: 150, message: '字符长度 最多 150', trigger: 'blur' },
        ],
        password:[
            { required: true, message: '请填写密码', trigger: 'change' },
            { min: 6, max: 16, message: '字符长度 6 到 16', trigger: 'blur' },
        ]
      },

    }
  },
  methods:{
    formSubmit(){
      this.$refs["form"].validate((valid) => {
        if (valid) {
          let username = this.form.username
          apiLogin(this.form).then(res=>{
            if (res.status == '200'){
              sessionStorage.setItem('token',res.token)
              sessionStorage.setItem('islogin',true)
              sessionStorage.setItem('ut',res.user_type)
              sessionStorage.setItem('username',username)
              ElMessage.success("登录成功")
              this.$router.replace({path:"/",query: { page: 'home' }})
            }else{
              ElMessage.error(res.msg)
            }
          })
        } else {
          console.log('error submit!')
          return false
        }
      })
    }
  },
  created() {
    if(Boolean(sessionStorage.getItem('islogin'))){
      this.$router.replace('/?page=home')
    }
  }
}
</script>

<style scoped>

</style>