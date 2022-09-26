<template>

    <el-container>

      <el-main>
        <el-table  v-loading="is_loading" :data="tableData" style="width: 100%">
          <template v-for="i in fields">
            <el-table-column v-if="i[1] !== 'property'" :key="i[1]" :prop="i[1]" :label="i[0]"  />
            <el-table-column v-else :key="i[1]" >
              <template #header>
                <span>{{i[0]}}</span>
              </template>
              <template #default="scope">
                <template v-for="v in getProperty(scope.$index, scope.row)" :key="v" >
                   <el-tag style="margin-left: 2px"  size="small">{{ v }}</el-tag>
                </template>

              </template>
            </el-table-column>
          </template>
          <el-table-column v-if="options" label="操作">
            <template #default="scope">
                <el-button
                  size="small"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>

          <el-table-column v-if="getPage === 'maintain'"  label="操作">
            <template #default="scope">
                <el-button
                  size="small"
                  :type="scope.row.maintenance_men_username !== '暂未维修' ? 'success' : 'warning'"
                  @click="ut === '2' ? handleMaintain(scope.$index, scope.row) : ()=>{} "
                  >{{ scope.row.maintenance_men_username !== '暂未维修' ? "已维修" : "未维修" }}</el-button
                >
              </template>
            </el-table-column>

        </el-table>
      </el-main>
      <el-footer>
        <el-pagination background @current-change="handleCurrentChange"  v-model="page_length.page" layout="prev, pager, next" :page-count="pageNum" />
      </el-footer>
    </el-container>

</template>

<script>
import HomePage from "@/components/Home";
import {apiGetUserInfos} from "@/apis/user";
import {ElMessage, ElMessageBox} from "element-plus";
import {
  apiGetCarports,
  apiGetCharge,
  apiGetComplaintMessage,
  apiGetMaintainMessage
} from "@/apis/getdatas";
import {apiDelCharge, apiDelComplaint, apiDelMaintain, apiDelUser} from "@/apis/deldatas";
import {apiUpdateMaintain} from "@/apis/utils";

export default {
  name: "ManageTable",
  computed:{
    getPage(){
      return this.$route.query.page
    },
    ut(){
      return sessionStorage.getItem('ut')
    },
    options(){
      if(this.ut === '1'){
        return this.$route.query.page === 'message'
            ||
            this.$route.query.page === 'maintain';
      }else if(this.ut === '2'){
        return false
      }else{
        return this.$route.query.page !== 'carport';
      }
    }
  },
  methods:{
    async getData() {
      this.is_loading = true;
      let dataTable
      switch (this.$route.query.page) {
        case "user":{
          await apiGetUserInfos(this.page_length).then(res => {
            if (res.status == '200') {
              dataTable = res.data.data
              this.fields = res.data.filed
              this.pageNum = res.data.pageNum
            }else{
                dataTable = []
                ElMessage.error(res.msg)
            }
          })
           break
        }

        case "carport":{
          await apiGetCarports(this.page_length).then(res => {
            if (res.status == '200') {
              dataTable = res.data.data
              this.fields = res.data.filed
              this.pageNum = res.data.pageNum
            }else{
                dataTable = []
                ElMessage.error(res.msg)
            }
          })
           break
        }
        case "message":{
          await apiGetComplaintMessage(this.page_length).then(res => {
            if (res.status == '200') {
              dataTable = res.data.data
              this.fields = res.data.filed
              this.pageNum = res.data.pageNum
            }else{
                dataTable = []
                ElMessage.error(res.msg)
            }
          })
           break
        }
        case "maintain":{
          await apiGetMaintainMessage(this.page_length).then(res => {
            if (res.status == '200') {
              dataTable = res.data.data
              this.fields = res.data.filed
              this.pageNum = res.data.pageNum
            }else{
                dataTable = []
                ElMessage.error(res.msg)
            }
          })
           break
        }
        case "charge":{
          await apiGetCharge(this.page_length).then(res => {
            if (res.status == '200') {
              dataTable = res.data.data
              this.fields = res.data.filed
              this.pageNum = res.data.pageNum
            }else{
                dataTable = []
                ElMessage.error(res.msg)
            }
          })
           break
        }
      }

      this.is_loading = false;
      this.tableData =  dataTable;
    },
    handleCurrentChange(currentPage) {
      //页码更改方法
      this.page_length.page = currentPage;
      this.getData()

    },
    getProperty(index, row){
      console.log(index, row)
      return this.tableData[index].property
    },
    handleDelete(index,row){
      console.log(index,row)
      switch (this.$route.query.page) {
        case "user":{
          ElMessageBox.alert('是否删除该用户', '删除用户', {
              // if you want to disable its autofocus
              // autofocus: false,
              confirmButtonText: 'OK',
              callback: (action) => {
                if(action!=='cancel'){
                  apiDelUser({id:row.username}).then(res=>{
                     if (res.status == '200'){
                      ElMessage.success("删除成功")
                    }else{
                      ElMessage.error(res.msg)
                    }
                     this.$router.go(0)
                  })
                }
              },
            })
          break
        }
        case "message":{
          apiDelComplaint({id:row.meta_id}).then(res=>{

              if (res.status == '200'){
                ElMessage.success("删除成功")
              }else{
                ElMessage.error(res.msg)
              }
              this.$router.go(0)

          })
          break
        }
        case "maintain":{
          apiDelMaintain({id:row.meta_id}).then(res=>{
            if (res.status == '200'){
              ElMessage.success("删除成功")
            }else{
              ElMessage.error(res.msg)
            }
            this.$router.go(0)
          })
          break
        }
        case "charge":{
          apiDelCharge({id:row.meta_id}).then(res=>{
            if (res.status == '200'){
              ElMessage.success("删除成功")
            }else{
              ElMessage.error(res.msg)
            }
            this.$router.go(0)
          })
          break
        }


      }
    },
    handleMaintain(index,row){
      apiUpdateMaintain({id:row.meta_id}).then(res=>{
        if (res.status == '200'){
              ElMessage.success("提交成功")
            }else{
              ElMessage.error(res.msg)
            }
            this.$router.go(0)
      })
    }
  },
  watch:{
    "$route.query.page"(){
       this.page_length.page = 1
       this.getData()
    }
  },
  data(){
    return {
      fields:[],
      tableData:[],
      is_loading:true,
      page_length:{
        page:1,
      },
      pageNum:1
    }
  },
  created() {
    this.getData()
  }
}
</script>

<style scoped>
section{
  height: auto;
}
</style>