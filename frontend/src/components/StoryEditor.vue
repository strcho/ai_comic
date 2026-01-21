<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElInput, ElCard } from 'element-plus'

const props = defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const text = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', value)
})

const wordCount = computed(() => text.value.split(/\s+/).filter(w => w.length > 0).length)
const charCount = computed(() => text.value.length)
</script>

<template>
  <el-card class="story-editor">
    <template #header>
      <div class="editor-header">
        <h3>Story Editor</h3>
        <span class="stats">
          {{ charCount }} chars · {{ wordCount }} words
        </span>
      </div>
    </template>
    
    <el-input
      v-model="text"
      type="textarea"
      :rows="15"
      :disabled="disabled"
      placeholder="Enter your story here... Separate scenes with blank lines or 'Scene:', 'Panel:', 'Frame:' markers."
      show-word-limit
      :maxlength="5000"
    />
    
    <div class="tips">
      <p><strong>Tips:</strong></p>
      <ul>
        <li>Use blank lines to separate scenes</li>
        <li>Or use markers like "Scene 1:", "Panel A:", etc.</li>
        <li>2-5 scenes work best</li>
      </ul>
    </div>
  </el-card>
</template>

<style scoped>
.story-editor {
  height: 100%;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-header h3 {
  margin: 0;
}

.stats {
  font-size: 0.875rem;
  color: #666;
}

.tips {
  margin-top: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
  font-size: 0.875rem;
}

.tips p {
  margin: 0 0 0.5rem 0;
}

.tips ul {
  margin: 0;
  padding-left: 1.5rem;
}

.tips li {
  margin-bottom: 0.25rem;
}
</style>