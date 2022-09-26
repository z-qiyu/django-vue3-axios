<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>登录</span>
        <el-button class="button" @click="$router.replace('/register')" text>没有账号? 注册</el-button>
      </div>
    </template>
    <LoginForm></LoginForm>
  </el-card>
</template>

<script>
import LoginForm from "@/components/LoginForm";


export default {
  name: "LoginView",
  components:{
    LoginForm
  }
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  span{
    font-weight: bold;
    font-size: 18px;
  }

}

.box-card{
  position: fixed;
  top: 10%;
  left:25%;
  width: 50%;
}
</style>