<template>
  <el-button class="back-btn-float" type="info" plain :icon="icon" @click="goBack"> 返回 </el-button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const icon = ArrowLeft
function goBack() {
  router.back()
}
</script>

<style scoped>
.back-btn-float {
  position: absolute;
  right: 32px;
  bottom: 32px;
  z-index: 10;
  border-radius: 50px;
  font-size: 1.08rem;
  font-weight: 600;
  letter-spacing: 1px;
  background: #f6f8fa;
  color: #409eff;
  border: 1.5px solid #dbeafe;
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.08);
  padding: 12px 28px;
  transition:
    background 0.2s,
    color 0.2s,
    box-shadow 0.2s;
}
.back-btn-float:hover {
  background: #e8f3ff;
  color: #67c23a;
  border-color: #67c23a;
  box-shadow: 0 8px 32px rgba(103, 194, 58, 0.13);
}
</style>
