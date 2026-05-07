<template>
  <div class="task-detail">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="progress-card">
          <template #header>执行进度</template>
          <AgentProgress :events="events" :current-status="taskStatus" />
        </el-card>

        <el-card class="info-card" style="margin-top: 16px">
          <template #header>任务信息</template>
          <p><strong>任务 ID：</strong>{{ taskId }}</p>
          <p><strong>研究议题：</strong>{{ taskQuery }}</p>
          <p><strong>状态：</strong>{{ taskStatus }}</p>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card v-if="taskStatus === 'completed' && reportContent">
          <template #header>
            <div class="report-header">
              <span>研报预览</span>
              <el-button size="small" @click="downloadReport">下载 Markdown</el-button>
            </div>
          </template>
          <ReportViewer :content="reportContent" />
        </el-card>

        <el-card v-else>
          <template #header>实时日志</template>
          <div class="log-stream">
            <div v-for="(event, i) in events" :key="i" class="log-entry">
              <el-tag :type="getTagType(event.agent)" size="small">{{ event.agent }}</el-tag>
              <span class="log-message">{{ event.status }}</span>
              <span class="log-time">{{ formatTime(event.timestamp) }}</span>
            </div>
            <div v-if="events.length === 0" class="empty-log">等待执行...</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTask, getReport, createEventSource } from '../api/client'
import AgentProgress from '../components/AgentProgress.vue'
import ReportViewer from '../components/ReportViewer.vue'

const route = useRoute()
const router = useRouter()
const taskId = route.params.id as string

const taskQuery = ref('')
const taskStatus = ref('running')
const reportContent = ref('')
const events = ref<Array<{ agent: string; status: string; timestamp: string }>>([])
let es: EventSource | null = null

onMounted(async () => {
  try {
    const task = await getTask(taskId)
    taskQuery.value = task.query
    taskStatus.value = task.status

    if (task.status === 'completed') {
      reportContent.value = await getReport(taskId)
      return
    }

    if (task.status === 'failed') {
      ElMessage.error('任务已失败')
      return
    }
  } catch (err: any) {
    if (err?.response?.status === 404) {
      ElMessage.error('任务不存在')
      router.push('/')
      return
    }
    ElMessage.error('加载任务失败')
    return
  }

  es = createEventSource(taskId)
  es.addEventListener('agent_progress', (e) => {
    events.value.push(JSON.parse(e.data))
  })
  es.addEventListener('agent_start', (e) => {
    events.value.push(JSON.parse(e.data))
  })
  es.addEventListener('agent_complete', (e) => {
    events.value.push(JSON.parse(e.data))
  })
  es.addEventListener('task_complete', async () => {
    taskStatus.value = 'completed'
    reportContent.value = await getReport(taskId)
  })
  es.addEventListener('agent_failed', (e) => {
    events.value.push(JSON.parse(e.data))
    taskStatus.value = 'failed'
  })
  es.onerror = () => {
    // SSE 连接断开时静默处理，任务可能已完成或失败
  }
})

onUnmounted(() => {
  es?.close()
})

function getTagType(agent: string): string {
  const map: Record<string, string> = {
    planner: '', researcher: 'success', synthesizer: 'warning', critic: 'danger', writer: 'info',
  }
  return map[agent] || ''
}

function formatTime(ts: string): string {
  return new Date(ts).toLocaleTimeString('zh-CN')
}

function downloadReport() {
  const blob = new Blob([reportContent.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `report-${taskId}.md`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.task-detail { padding: 20px; }
.progress-card, .info-card { margin-bottom: 16px; }
.report-header { display: flex; justify-content: space-between; align-items: center; }
.log-stream { max-height: 500px; overflow-y: auto; }
.log-entry { padding: 8px 0; display: flex; align-items: center; gap: 10px; }
.log-message { flex: 1; }
.log-time { color: #909399; font-size: 12px; }
.empty-log { color: #c0c4cc; text-align: center; padding: 40px; }
</style>
