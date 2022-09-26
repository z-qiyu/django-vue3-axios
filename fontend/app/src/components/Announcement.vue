<template>
  <el-container>
      <el-header style="text-align: start">
        <h3>公告 & 历史公告</h3>
      </el-header>
      <el-main>
        <el-card v-if="ut === '3'" style="margin-bottom: 20px;text-align: start" class="box-card">
          <template #header>
            <div class="card-header">
              <span>创建公告</span>
              <el-button class="button" @click="createAnnouncement" type="primary">创建</el-button>
            </div>
          </template>
          <div class="text item">
            <el-form
                :label-position="left"
                label-width="100px"
                :model="form"
                style="max-width: 460px"
                :rules="rules"
                ref="form"
            >
              <el-form-item label="标题" prop="title">
                <el-input v-model="form.title" />
              </el-form-item>
              <el-form-item label="内容" prop="content">
                <el-input v-model="form.content" />
              </el-form-item>
            </el-form>
          </div>
        </el-card>
        <el-timeline>
          <el-timeline-item v-for="i in data" :key="i" :timestamp="i.time" placement="top">
            <el-card>
              <h4>{{i.title}}</h4>
              <p>{{i.content}}</p>
               <div
                style="display: flex;flex-direction: row-reverse"
               ><el-button
                 v-if="ut === '3'"
                  size="small"
                  type="danger"
                  @click="handleDelete(i.meta_id)"
                  >Delete</el-button
                ></div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-main>
    </el-container>

</template>

<script>
import {apiGetAnnouncement} from "@/apis/getdatas";
import {ElMessage} from "element-plus";
import {apiPutAnnouncement} from "@/apis/utils";
import {apiDelAnnouncement} from "@/apis/deldatas";

export default {
  name: "Announcement",
  data(){
    return {
      form:{
        title:"",
        content:""
      },
      rules:{
        title:[
            { required: true, message: '请填写标题', trigger: 'change' },
            { min: 0, max: 20, message: '字符长度 最多 20', trigger: 'blur' },
        ],
        content:[
            { required: true, message: '请填写内容', trigger: 'change' },
            { min: 0, max: 128, message: '字符长度 最多 128', trigger: 'blur' },
        ]
      },
      data:[]
    }
  },
  methods:{
    createAnnouncement(){
      this.$refs['form'].validate(valid => {
        if(valid){
          apiPutAnnouncement(this.form).then(res=>{
            if (res.status == '200'){
              ElMessage.success("发布公告成功")
              this.$router.go(0)
            }else{
              ElMessage.error(res.msg)
            }
          })
        }else{
          ElMessage.error('注意填写约束')
          return false
        }
      })
    },
    handleDelete(id){
      console.log(id)
      apiDelAnnouncement({id:id}).then(res=>{
        if (res.status == '200'){
          ElMessage.success("删除成功")
        }else{
          ElMessage.error(res.msg)
        }
      })

    }
  },
  computed:{
    ut(){
      return sessionStorage.getItem('ut')
    },
  },
  created() {
    apiGetAnnouncement({}).then(res => {
      if (res.status == '200') {
          this.data = res.data.data
      }else{
          ElMessage.error(res.msg)
      }
    })
  }
}
</script>

<style>
.el-timeline-item__timestamp, .el-card__body{
  text-align: start;
}
</style>

<style scoped>

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
