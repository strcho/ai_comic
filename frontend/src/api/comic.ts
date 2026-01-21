import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Scene {
  id: number
  description: string
  cleaned_description: string
  image_prompt?: string
  image_url?: string
  image_path?: string
}

export interface ComicRequest {
  text: string
  style?: string
  image_size?: number
  format?: string
  quality?: string
}

export interface ComicResponse {
  id: string
  status: string
  progress: number
  scenes: Scene[]
  output_path?: string
  error?: string
  created_at: string
}

export const comicApi = {
  async generateComic(request: ComicRequest): Promise<ComicResponse> {
    const response = await api.post('/api/generate', request)
    return response.data.data
  },

  async getTaskStatus(taskId: string): Promise<ComicResponse> {
    const response = await api.get(`/api/task/${taskId}`)
    return response.data.data
  },

  async getHistory(): Promise<ComicResponse[]> {
    const response = await api.get('/api/history')
    return response.data.data
  },

  async downloadComic(taskId: string): Promise<Blob> {
    const response = await api.get(`/api/comic/${taskId}`, {
      responseType: 'blob',
    })
    return response.data
  },
}