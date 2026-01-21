<script setup lang="ts">
import { ref } from 'vue'
import { ElCard, ElButton, ElImage } from 'element-plus'
import type { ComicResponse } from '../api/comic'

const props = defineProps<{
  comic: ComicResponse
  isCompleted: boolean
}>()

const emit = defineEmits<{
  (e: 'download'): void
}>()

const currentScene = ref(0)

const handleDownload = () => {
  emit('download')
}

const prevScene = () => {
  if (currentScene.value > 0) {
    currentScene.value--
  }
}

const nextScene = () => {
  if (currentScene.value < props.comic.scenes.length - 1) {
    currentScene.value++
  }
}
</script>

<template>
  <div class="comic-preview">
    <div v-if="!isCompleted" class="scene-list">
      <h3>Generated Scenes</h3>
      <div v-for="(scene, index) in comic.scenes" :key="scene.id" class="scene-item">
        <div class="scene-header">
          <span class="scene-number">Scene {{ scene.id }}</span>
        </div>
        <div class="scene-content">
          <p class="scene-description">{{ scene.description }}</p>
          <div v-if="scene.image_url" class="scene-image">
            <el-image :src="scene.image_url" fit="contain" />
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="completed-comic">
      <div class="comic-header">
        <h3>Your Comic</h3>
        <el-button type="primary" @click="handleDownload">
          Download
        </el-button>
      </div>
      
      <div v-if="comic.output_path" class="final-comic">
        <el-image
          :src="`/api/comic/${comic.id}`"
          fit="contain"
          :preview-src-list="[`/api/comic/${comic.id}`]"
        />
      </div>
      
      <div class="scene-preview">
        <div class="scene-controls">
          <el-button @click="prevScene" :disabled="currentScene === 0">
            Previous
          </el-button>
          <span>Scene {{ currentScene + 1 }} / {{ comic.scenes.length }}</span>
          <el-button @click="nextScene" :disabled="currentScene === comic.scenes.length - 1">
            Next
          </el-button>
        </div>
        
        <div class="scene-info">
          <p>{{ comic.scenes[currentScene]?.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comic-preview {
  height: 100%;
}

.scene-list h3,
.completed-comic .comic-header h3 {
  margin: 0 0 1rem 0;
}

.scene-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 6px;
}

.scene-header {
  margin-bottom: 0.75rem;
}

.scene-number {
  font-weight: bold;
  color: #409eff;
}

.scene-description {
  margin: 0 0 0.75rem 0;
  font-style: italic;
  color: #666;
}

.scene-image {
  text-align: center;
}

.comic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.final-comic {
  text-align: center;
  margin-bottom: 2rem;
}

.scene-preview {
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
}

.scene-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.scene-info {
  text-align: center;
  color: #666;
}

.scene-info p {
  margin: 0;
}
</style>