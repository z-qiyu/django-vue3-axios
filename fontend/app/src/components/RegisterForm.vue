<template>
  <div>
    <el-form
      label-position="left"
      label-width="130px"
      :model="form"
      style="max-width: 460px"
      :rules="rules"
      ref="form"
    >
      <el-form-item label="用户名" prop="username"  required>
        <el-input v-model="form.username" type="text" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email" required>
        <el-input v-model="form.email" type="email" />
      </el-form-item>
      <el-form-item label="电话号码" prop="tel" required>
        <el-input v-model="form.tel" type="number" />
      </el-form-item>
      <el-form-item label="性别" prop="gender"  required>
        <el-radio-group v-model="form.gender">
          <el-radio-button label="男" value="1" />
          <el-radio-button label="女" value="2" />
        </el-radio-group>
      </el-form-item>
      <el-form-item label="是否注册维修员" prop="user_type">
        <el-switch
          v-model="form.user_type"
          inline-prompt
          active-text="是"
          inactive-text="否"
        />
      </el-form-item>
      <el-form-item label="密码" prop="password" required>
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item label="确认密码" prop="re_password" required>
        <el-input v-model="form.re_password" type="password" />
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="formSubmit">注册</el-button>
  </div>
</template>

<script>
import {apiRegister} from "@/apis/user";
import {ElMessage} from "element-plus";

export default {
  name: "RegisterForm",
  data(){
    return {
      form:{
        username:"",
        gender:"",
        user_type:false, // false 用户 ,true 维修员
        email:"",
        tel:null,
        password:"",
        re_password:""
      },
      rules:{
        username:[
            { required: true, message: '请填写用户名', trigger: 'change' },
            { min: 0, max: 150, message: '字符长度 最多 150', trigger: 'blur' },
        ],
        password:[
            { required: true, message: '请填写密码', trigger: 'change' },
            { min: 6, max: 16, message: '字符长度 6 到 16', trigger: 'blur' },
        ],
        gender:[
            { required: true, message: '请填写性别', trigger: 'change' },
        ],
        tel:[
            { required: true, message: '请填写电话号码', trigger: 'change' },
            { min: 11, max: 11, message: '字符长度 11 位', trigger: 'blur' },
        ],
        re_password: [
          { required: true, message: '请填写确认密码', trigger: 'change' },
          {validator:(rule, value, callback)=>{
              if(value !== this.form.password){
                callback(new Error("两次密码不一样!"))
              }else{
                callback()
              }
            }, trigger: 'blur'}
        ],
        email:[
          {validator:(rule,value,callback) => {
            const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
            if(regEmail.test(value)){
              return callback();
            }
            callback(new Error('请输入合法的邮箱！'));
          }, trigger: 'blur'}
        ]
      },

    }
  },
  methods:{
    formSubmit(){
      this.$refs["form"].validate((valid) => {
        if (valid) {
          apiRegister(this.form).then(res=>{
            if (res.status == '200'){
              ElMessage.success("注册成功")
              this.$router.replace('/login')
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
  }
}
</script>

<style scoped>

</style>