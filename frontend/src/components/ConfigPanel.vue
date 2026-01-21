<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElCard, ElForm, ElFormItem, ElSelect, ElOption, ElSlider } from 'element-plus'
import type { ComicRequest } from '../api/comic'

const props = defineProps<{
  modelValue: ComicRequest
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: ComicRequest): void
}>()

const config = computed({
  get: () => props.modelValue,
  set: (value: ComicRequest) => emit('update:modelValue', value)
})

const updateConfig = (key: keyof ComicRequest, value: any) => {
  emit('update:modelValue', { ...config.value, [key]: value })
}
</script>

<template>
  <el-card class="config-panel">
    <template #header>
      <h3>Generation Config</h3>
    </template>
    
    <el-form label-position="top">
      <el-form-item label="Style">
        <el-select
          :model-value="config.style"
          :disabled="disabled"
          @update:model-value="updateConfig('style', $event)"
        >
          <el-option label="Vivid" value="vivid" />
          <el-option label="Natural" value="natural" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="Image Size">
        <el-slider
          :model-value="config.image_size"
          :disabled="disabled"
          :min="256"
          :max="1024"
          :step="128"
          show-stops
          show-input
          @update:model-value="updateConfig('image_size', $event)"
        />
      </el-form-item>
      
      <el-form-item label="Output Format">
        <el-select
          :model-value="config.format"
          :disabled="disabled"
          @update:model-value="updateConfig('format', $event)"
        >
          <el-option label="PNG" value="png" />
          <el-option label="PDF" value="pdf" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="Quality">
        <el-select
          :model-value="config.quality"
          :disabled="disabled"
          @update:model-value="updateConfig('quality', $event)"
        >
          <el-option label="Standard" value="standard" />
          <el-option label="HD" value="hd" />
        </el-select>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<style scoped>
.config-panel {
  margin-top: 1rem;
}

.config-panel h3 {
  margin: 0;
}
</style>