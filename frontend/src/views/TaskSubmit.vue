<template>
  <div class="task-submit">
    <el-row justify="center">
      <el-col :span="16">
        <h2>新建研究任务</h2>
        <p class="subtitle">输入研究议题，AI 将自动拆解、搜索、分析并生成研报</p>

        <el-input
          v-model="query"
          type="textarea"
          :rows="4"
          placeholder="例如：分析 2026 Q1 全球人形机器人市场格局"
          class="query-input"
        />

        <div class="examples">
          <span class="label">示例：</span>
          <el-tag
            v-for="example in examples"
            :key="example"
            class="example-tag"
            @click="query = example"
          >
            {{ example }}
          </el-tag>
        </div>

        <el-button
          type="primary"
          size="large"
          :loading="submitting"
          :disabled="!query.trim()"
          @click="submitTask"
        >
          开始研究
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createTask } from '../api/client'

const router = useRouter()
const query = ref('')
const submitting = ref(false)

const examples = [
  '分析 2026 Q1 全球人形机器人市场格局',
  '半导体设备国产化替代进展与竞争分析',
  '2026年全球新能源汽车电池技术路线对比',
]

async function submitTask() {
  if (!query.value.trim()) return
  submitting.value = true
  try {
    const { task_id } = await createTask(query.value)
    router.push(`/task/${task_id}`)
  } catch (err) {
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.task-submit {
  padding: 60px 0;
  text-align: center;
}
.subtitle {
  color: #909399;
  margin-bottom: 30px;
}
.query-input {
  margin-bottom: 20px;
}
.examples {
  margin-bottom: 30px;
}
.examples .label {
  color: #909399;
  margin-right: 10px;
}
.example-tag {
  cursor: pointer;
  margin: 0 5px;
}
</style>
