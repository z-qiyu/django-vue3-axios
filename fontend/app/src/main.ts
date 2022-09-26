import { createApp } from 'vue'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue'
import axios from "axios";
import './registerServiceWorker'
import router from './router'


let app = createApp(App)

app.config.globalProperties.$axios = axios

app.use(router)
app.use(ElementPlus)
app.mount('#app')
