<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>注册</span>
        <el-button class="button" @click="$router.replace('/login')" text>已有账号! 登录</el-button>
      </div>
    </template>
    <RegisterForm></RegisterForm>
  </el-card>
</template>

<script>
import RegisterForm from "@/components/RegisterForm";

export default {
  name: "RegisterView",
  components:{
    RegisterForm
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