import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

import TaskSubmit from './views/TaskSubmit.vue'
import TaskDetail from './views/TaskDetail.vue'
import ReportList from './views/ReportList.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: TaskSubmit },
    { path: '/task/:id', component: TaskDetail },
    { path: '/reports', component: ReportList },
  ],
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
