import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export interface Task {
  id: string
  query: string
  status: string
  created_at: string
  completed_at?: string
  report_path?: string
}

export async function createTask(query: string): Promise<{ task_id: string }> {
  const resp = await api.post('/tasks', { query })
  return resp.data
}

export async function getTask(taskId: string): Promise<Task> {
  const resp = await api.get(`/tasks/${taskId}`)
  return resp.data
}

export async function listTasks(limit = 20, offset = 0): Promise<Task[]> {
  const resp = await api.get('/tasks', { params: { limit, offset } })
  return resp.data
}

export async function getReport(taskId: string): Promise<string> {
  const resp = await api.get(`/reports/${taskId}`, { responseType: 'text' })
  return resp.data
}

export function createEventSource(taskId: string): EventSource {
  return new EventSource(`/api/tasks/${taskId}/stream`)
}
