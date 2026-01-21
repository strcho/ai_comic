<script setup lang="ts">
import { ref } from 'vue'
import { useComicStore } from '../stores/comic'
import StoryEditor from '../components/StoryEditor.vue'
import ComicPreview from '../components/ComicPreview.vue'
import ProgressDisplay from '../components/ProgressDisplay.vue'
import ConfigPanel from '../components/ConfigPanel.vue'

const comicStore = useComicStore()
const storyText = ref('')
const config = ref({
  style: 'vivid',
  image_size: 1024,
  format: 'png',
  quality: 'standard',
})

comicStore.loadHistory()

async function handleGenerate() {
  if (!storyText.value.trim()) return
  
  await comicStore.generateComic({
    text: storyText.value,
    ...config.value,
  })
}

function handleReset() {
  comicStore.reset()
}
</script>

<template>
  <div class="home">
    <header class="header">
      <h1>Comic Generation Agent</h1>
      <p>Transform your stories into comics using AI</p>
    </header>
    
    <main class="main">
      <div class="editor-section">
        <StoryEditor 
          v-model="storyText" 
          :disabled="comicStore.isGenerating"
        />
        
        <ConfigPanel 
          v-model="config"
          :disabled="comicStore.isGenerating"
        />
        
        <div class="actions">
          <el-button 
            type="primary" 
            size="large"
            :loading="comicStore.isGenerating"
            @click="handleGenerate"
            :disabled="!storyText.trim()"
          >
            Generate Comic
          </el-button>
          
          <el-button 
            v-if="comicStore.currentComic"
            @click="handleReset"
          >
            Reset
          </el-button>
        </div>
      </div>
      
      <div class="preview-section">
        <ProgressDisplay 
          v-if="comicStore.isGenerating"
          :progress="comicStore.progress"
        />
        
        <ComicPreview 
          v-if="comicStore.currentComic"
          :comic="comicStore.currentComic"
          :is-completed="comicStore.isCompleted"
          @download="comicStore.downloadComic"
        />
      </div>
    </main>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
}

.header p {
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.9;
}

.main {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

.editor-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.preview-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  min-height: 400px;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

@media (max-width: 968px) {
  .main {
    grid-template-columns: 1fr;
  }
}
</style>