<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header">
            <el-page-header  @back="logout"  icon>
              <template #title>
                 <el-button
                    type="danger"
                    text
                    >退出登陆</el-button
                  >
              </template>
              <template #content>
                <span class="text-large font-600 mr-3"> {{username}} </span>
              </template>
            </el-page-header>
        </el-header>

      <el-container>
         <el-aside width="200px">
          <el-menu
            background-color="#2c3e50"
            text-color="#fff"
            :default-active="$route.path + '?page=home'"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            router
          >
            <el-button style="width: 100%" type="text" :icon="btnIcon" @click="Collapse">
            </el-button>
            <el-menu-item :route="{ path: $route.path, query: { page: 'home' } }" index="1">
              <el-icon><Home /></el-icon>
              <template #title>个人信息</template>
            </el-menu-item>
            <el-menu-item v-if="ut === '3'" :route="{ path: $route.path, query: { page: 'user' } }" index="2">
              <el-icon><User /></el-icon>
              <template #title>用户管理</template>
            </el-menu-item>
            <el-menu-item v-if="ut === '3' || ut === '1' " :route="{ path: $route.path, query: { page: 'carport' } }" index="3">
              <el-icon><Van /></el-icon>
              <template #title>车位管理</template>
            </el-menu-item>
            <el-menu-item :route="{ path: $route.path, query: { page: 'message' } }" index="4">
              <el-icon><Message /></el-icon>
              <template #title>投诉信息</template>
            </el-menu-item>
            <el-menu-item :route="{ path: $route.path, query: { page: 'maintain' } }" index="5">
              <el-icon><Setting /></el-icon>
              <template #title>维修信息</template>
            </el-menu-item>
            <el-menu-item v-if="ut !== '2'" :route="{ path: $route.path, query: { page: 'charge' } }" index="6">
              <el-icon><Coin /></el-icon>
              <template #title>收费信息</template>
            </el-menu-item>
            <el-menu-item :route="{ path: $route.path, query: { page: 'announcement' } }" index="7">
              <el-icon><DataBoard /></el-icon>
              <template #title>公告</template>
            </el-menu-item>
            <el-menu-item :route="{ path: $route.path, query: { page: 'abstract' } }" index="8">
              <el-icon><InfoFilled /></el-icon>
              <template #title>系统简介</template>
            </el-menu-item>
          </el-menu>
      </el-aside>
        <el-main>
            <component :is="cpt"></component>
        </el-main>
      </el-container>
    </el-container>
  </div>
  <el-col>

    <el-row>

    </el-row>
  </el-col>
</template>

<script>

import {
  ArrowRight,
  ArrowLeft,
  User,
  Message,
  Setting,
  Van,
  Coin,
  DataBoard,
  InfoFilled,
  HomeFilled as Home,
} from '@element-plus/icons-vue'
import ManageTable from "@/components/ManageTable";
import HomePage from "@/components/Home"
import Abstract from "@/components/Abstract";
import Announcement from "@/components/Announcement";
import {useCookies} from "@vueuse/integrations/useCookies"

const cookie = useCookies();

export default {
  name:"ManageView",
  data(){
    return {
      isCollapse:false,
      username:sessionStorage.getItem("username")
    }
  },
  computed:{
    cpt(){
      switch (this.$route.query.page) {
        case "home": return HomePage
        case "user": return ManageTable
        case "carport": return ManageTable
        case "message": return ManageTable
        case "maintain": return ManageTable
        case "charge": return ManageTable
        case "announcement": return Announcement
        case "abstract": return Abstract
      }
    },
    ut(){
      return sessionStorage.getItem("ut")
    },
    btnIcon(){
      return this.isCollapse ? ArrowLeft : ArrowRight
    }
  },
  methods:{
    Collapse(){
      this.isCollapse = !this.isCollapse
    },
    logout(){
      sessionStorage.removeItem("token")
      sessionStorage.removeItem("islogin")
      this.$router.replace('/login')
    }
  },
  created() {
    if(sessionStorage.getItem("islogin")){

    }else{
      this.$router.replace("/login")
    }
  },
  components:{
    ArrowRight,
    ArrowLeft,
    User,
    Message,
    Setting,
    Van,
    ManageTable,
    Coin,
    DataBoard,
    InfoFilled,
    Home
  }

}


</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
body,#app,html{
  margin: 0;
  width: 100%;
  height: 100%;
}
.common-layout,section{
  height: 100%;
}
</style>

<style lang="scss" scoped>
.header{
  box-shadow: 1px 1px 4px 2px rgba(0,0,0,.3);
}
.el-menu[role="menubar"]{
  height: 100%;
}

</style>
