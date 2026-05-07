<template>
  <div class="report-list">
    <h2>历史报告</h2>

    <el-table :data="tasks" v-loading="loading" stripe>
      <el-table-column prop="id" label="任务 ID" width="280" show-overflow-tooltip />
      <el-table-column prop="query" label="研究议题" min-width="300" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'completed'"
            type="primary"
            link
            @click="$router.push(`/task/${row.id}`)"
          >
            查看报告
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listTasks, Task } from '../api/client'

const tasks = ref<Task[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    tasks.value = await listTasks()
  } finally {
    loading.value = false
  }
})

function statusType(status: string): string {
  const map: Record<string, string> = {
    pending: 'info', running: 'warning', completed: 'success', failed: 'danger',
  }
  return map[status] || ''
}

function statusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: '等待中', running: '执行中', completed: '已完成', failed: '失败',
  }
  return map[status] || status
}
</script>

<style scoped>
.report-list { padding: 20px; }
.report-list h2 { margin-bottom: 20px; }
</style>
