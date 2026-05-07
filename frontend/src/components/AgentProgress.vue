<template>
  <div class="agent-progress">
    <el-steps :active="activeStep" direction="vertical" finish-status="success">
      <el-step
        v-for="agent in agents"
        :key="agent.key"
        :title="agent.label"
        :description="getAgentStatus(agent.key)"
        :status="getStepStatus(agent.key)"
      />
    </el-steps>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  events: Array<{ agent: string; status: string; timestamp: string }>
  currentStatus: string
}>()

const agents = [
  { key: 'planner', label: '任务拆解' },
  { key: 'researcher', label: '信息采集' },
  { key: 'synthesizer', label: '综合分析' },
  { key: 'critic', label: '质量审查' },
  { key: 'writer', label: '报告撰写' },
]

const activeStep = computed(() => {
  const agentIndex: Record<string, number> = {
    planner: 0, researcher: 1, synthesizer: 2, critic: 3, writer: 4,
  }
  const lastEvent = [...props.events].reverse().find(e => e.agent in agentIndex)
  if (!lastEvent) return 0
  return (agentIndex[lastEvent.agent] || 0) + 1
})

function getAgentStatus(agentKey: string): string {
  const agentEvents = props.events.filter(e => e.agent === agentKey)
  if (agentEvents.length === 0) return '等待中...'
  const last = agentEvents[agentEvents.length - 1]
  return last.status
}

function getStepStatus(agentKey: string): string {
  const agentEvents = props.events.filter(e => e.agent === agentKey)
  if (agentEvents.length === 0) return 'wait'
  const last = agentEvents[agentEvents.length - 1]
  if (last.status === 'completed' || last.status.includes('完成')) return 'success'
  if (last.status === 'failed') return 'error'
  return 'process'
}
</script>
