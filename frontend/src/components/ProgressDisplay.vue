<script setup lang="ts">
import { ElProgress, ElAlert } from 'element-plus'

const props = defineProps<{
  progress: number
}>()
</script>

<template>
  <div class="progress-display">
    <el-alert
      title="Generating Comic..."
      type="info"
      :closable="false"
      show-icon
    >
      <el-progress
        :percentage="progress"
        :stroke-width="20"
        :text-inside="true"
        status="success"
      />
    </el-alert>
    
    <div class="progress-details">
      <p>Processing your story and generating images...</p>
      <p class="small">This may take 1-2 minutes depending on scene count.</p>
    </div>
  </div>
</template>

<style scoped>
.progress-display {
  padding: 2rem;
}

.progress-details {
  text-align: center;
  margin-top: 1.5rem;
}

.progress-details p {
  margin: 0.5rem 0;
  font-size: 1rem;
}

.progress-details .small {
  font-size: 0.875rem;
  color: #666;
}
</style>