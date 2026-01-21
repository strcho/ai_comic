import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { comicApi, type ComicRequest, type ComicResponse } from '../api/comic'

export const useComicStore = defineStore('comic', () => {
  const currentComic = ref<ComicResponse | null>(null)
  const isGenerating = ref(false)
  const error = ref<string | null>(null)
  const history = ref<ComicResponse[]>([])
  const pollInterval = ref<number | null>(null)

  const progress = computed(() => currentComic.value?.progress ?? 0)
  const isCompleted = computed(() => currentComic.value?.status === 'completed')
  const isFailed = computed(() => currentComic.value?.status === 'failed')

  async function generateComic(request: ComicRequest) {
    try {
      isGenerating.value = true
      error.value = null
      const result = await comicApi.generateComic(request)
      currentComic.value = result
      
      if (result.status !== 'completed' && result.status !== 'failed') {
        startPolling(result.id)
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to generate comic'
      throw e
    } finally {
      isGenerating.value = false
    }
  }

  function startPolling(taskId: string) {
    pollInterval.value = window.setInterval(async () => {
      try {
        const updated = await comicApi.getTaskStatus(taskId)
        currentComic.value = updated
        
        if (updated.status === 'completed' || updated.status === 'failed') {
          stopPolling()
          await loadHistory()
        }
      } catch (e) {
        console.error('Polling error:', e)
      }
    }, 2000)
  }

  function stopPolling() {
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
      pollInterval.value = null
    }
  }

  async function loadHistory() {
    try {
      history.value = await comicApi.getHistory()
    } catch (e) {
      console.error('Failed to load history:', e)
    }
  }

  async function downloadComic(taskId: string) {
    try {
      const blob = await comicApi.downloadComic(taskId)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `comic_${taskId}.png`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to download comic'
    }
  }

  function reset() {
    currentComic.value = null
    error.value = null
    stopPolling()
  }

  return {
    currentComic,
    isGenerating,
    error,
    history,
    progress,
    isCompleted,
    isFailed,
    generateComic,
    loadHistory,
    downloadComic,
    reset,
  }
})