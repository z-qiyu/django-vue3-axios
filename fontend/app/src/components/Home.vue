<template>
  <div>
  <el-descriptions
    title="我的信息"
    direction="vertical"
    :column="3"
    size="large"
    border
  >
    <el-descriptions-item label="用户名">
      {{data.username}}
      <el-button type="danger" @click="dialogFormVisible = true" style="margin-left: 10px" size="small">注销</el-button>
    </el-descriptions-item>
    <el-descriptions-item label="电话号码">{{data.tel}}</el-descriptions-item>
    <el-descriptions-item label="邮箱" >{{data.email}}</el-descriptions-item>
    <el-descriptions-item label="用户类型">
      <el-tag size="small">{{ data.ut }}</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="性别">{{data.gender}}</el-descriptions-item>
    <el-descriptions-item label="车位个数">{{data.carport}}</el-descriptions-item>
    <el-descriptions-item v-if="ut === '1'" span="3" label="资产">
      <template v-if="data.property.length !== 0">
        <template v-for="v in data.property" :key="v">
          <el-tag style="margin-left: 2px"  size="small">{{v}}</el-tag>
        </template>
      </template>
      <el-tag v-else style="margin-left: 2px"  size="small">无</el-tag>
    </el-descriptions-item>
    <el-descriptions-item v-if="ut === '1'" span="3" label="投诉">
       <el-row align="middle" justify="start" gutter="20">
         <el-col :span="16">
           <el-input :rows="2" type="textarea" v-model="complaintMessage" placeholder="输入投诉信息" />
         </el-col>
         <el-col :span="4">
           <el-button @click="complaintSubmit" type="danger">投诉</el-button>
         </el-col>

       </el-row>
    </el-descriptions-item>
    <el-descriptions-item v-if="ut === '1'" span="3" label="报修">
       <el-row align="middle" justify="start" gutter="20">
         <el-col :span="16">
           <el-input :rows="2" type="textarea" v-model="maintainMessage" placeholder="输入报修备注" />
         </el-col>
         <el-col :span="4">
           <el-button @click="maintainSubmit" type="primary">报修</el-button>
         </el-col>

       </el-row>
    </el-descriptions-item>
    <el-descriptions-item v-if="ut === '1'" span="3" label="缴费">
       <el-row align="middle" justify="start" gutter="20">
         <el-col :span="10">
           <el-radio-group v-model="charge.type" class="ml-4">
            <el-radio label="1" size="large">物业费</el-radio>
            <el-radio label="2" size="large">水费</el-radio>
             <el-radio label="3" size="large">车位费</el-radio>
          </el-radio-group>
         </el-col>
         <el-col :span="6">
           <el-input :rows="2" type="number" v-model="charge.money" placeholder="缴费金额" />
         </el-col>
         <el-col :span="4">
           <el-button @click="chargeSubmit" type="primary">缴费</el-button>
         </el-col>

       </el-row>
    </el-descriptions-item>

    <el-descriptions-item v-if="ut === '1'" span="3" label="设置资产">
       <el-row align="middle" justify="start" gutter="20">
         <el-col :span="10">
           <el-tag v-for="(v,i) in add_p_form.t" @click="del_t(i)" :key="i">
             {{ v }}
           </el-tag>
         </el-col>
         <el-col :span="6">
           <el-button @click="add_t" type="success">添加</el-button>
         </el-col>
         <el-col :span="4">
           <el-button @click="addPropertySubmit" type="primary">提交</el-button>
         </el-col>

       </el-row>
    </el-descriptions-item>

  </el-descriptions>

    <el-dialog v-model="addFormVisible" title="添加资产">
      <el-form >
        <el-form-item label="资产名称" label-width="100px">
          <el-input v-model="p" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="addFormVisible = false">取消</el-button>
          <el-button type="success" @click="addFormVisible = false; add_p_form.t.push(p)"
            >添加</el-button
          >
        </span>
      </template>
    </el-dialog>
  <el-dialog v-model="dialogFormVisible" title="用户注销">
      <el-form :model="delUserForm">
        <el-form-item label="密码确认" label-width="100px">
          <el-input v-model="delUserForm.password" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="dialogFormVisible = false">取消</el-button>
          <el-button type="danger" @click="writeOff();dialogFormVisible = false"
            >注销!</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>


import {apiAddProperty, apiDelete, apiGetUserInfo} from "@/apis/user";
import {ElMessage, ElMessageBox} from "element-plus";
import {apiPutCharge, apiPutComplaint, apiPutMaintain} from "@/apis/utils";

export default {
  name: "Home",
  data(){
    return {
      data:{
        username:"",
        email:"",
        tel:"",
        ut:"",
        gender:"",
        property:{
          data:[]
        }

      },
      complaintMessage:"",
      maintainMessage:"",
      charge:{
        type:"",
        money:null
      },
      add_p_form:{
        t:[]
      },
      dialogFormVisible:false,
      delUserForm:{
        password:""
      },
      addFormVisible:false,
      p:""
    }
  },
  methods:{
    writeOff(){
      apiDelete(this.delUserForm).then(res=>{
        if (res.status == '200'){
            ElMessageBox.alert('注销成功，确认刷新', '注销', {
              // if you want to disable its autofocus
              // autofocus: false,
              confirmButtonText: 'OK',
              callback: (action) => {
                  sessionStorage.removeItem("token")
                  sessionStorage.removeItem("islogin")
                  this.$router.replace('/login')
              },
            })
          }else{
            ElMessage.error(res.msg)
          }
        this.$router.replace('/login')
      })
    },
    complaintSubmit(){
      apiPutComplaint({msg:this.complaintMessage}).then(res=>{
         if (res.status == '200'){
            ElMessage.success("投诉成功")
          }else{
            ElMessage.error(res.msg)
          }
      })
    },
    maintainSubmit(){
      apiPutMaintain({msg:this.maintainMessage}).then(res=>{
         if (res.status == '200'){
            ElMessage.success("抱修成功")
          }else{
            ElMessage.error(res.msg)
          }
      })
    },
    chargeSubmit(){
       apiPutCharge(this.charge).then(res=>{
         if (res.status == '200'){
            ElMessage.success("缴费成功")
          }else{
            ElMessage.error(res.msg)
          }
      })
    },
    addPropertySubmit(){
      apiAddProperty(this.add_p_form).then(res=>{
          if (res.status == '200'){
            ElMessage.success("设置成功")
            this.$router.go(0)
          }else{
            ElMessage.error(res.msg)
          }
      })
    },
    add_t(){
      // this.add_p_form.t.push(t)
      this.addFormVisible = true
    },
    del_t(i){
      delete this.add_p_form.t[i]
      this.add_p_form.t.length-=1
    }
  },
  created() {
    apiGetUserInfo({}).then(res=>{
      if (res.status == '200'){

        this.data=res.data
        this.add_p_form.t = [].concat(this.data.property)

      }else{
        ElMessage.error(res.msg)
      }
    })
  },
  computed:{
    ut(){
      return sessionStorage.getItem("ut")
    },
  }
}
</script>

<style scoped>

</style>