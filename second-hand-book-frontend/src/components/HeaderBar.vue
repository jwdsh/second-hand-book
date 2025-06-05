<template>
  <el-header class="app-header">
    <span class="app-title">
      <el-icon style="margin-right: 14px; font-size: 2.4rem; vertical-align: middle">
        <Reading />
      </el-icon>
      二手书定价系统
    </span>
    <slot></slot>
  </el-header>
</template>

<script setup lang="ts">
import { Reading } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-header {
  color: #fff;
  padding: 100px 0 0 0;
  text-align: center;
  position: relative;
  letter-spacing: 2.5px;
}
.app-title {
  font-size: 2.6rem;
  font-weight: 900;
  text-shadow:
    0 4px 24px rgba(64, 158, 255, 0.13),
    0 2px 8px rgba(103, 194, 58, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
</style>
