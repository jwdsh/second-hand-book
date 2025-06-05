<script setup lang="ts">
import HeaderBar from '@/components/HeaderBar.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="background">
    <div class="background-mask"></div>
    <div class="app-container">
      <HeaderBar />
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.background {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: -2;
  background:
    radial-gradient(circle at 20% 30%, #6dd5fa 0%, #409eff 40%, transparent 80%),
    radial-gradient(circle at 80% 70%, #a8e063 0%, #67c23a 40%, transparent 80%),
    linear-gradient(90deg, #409eff 0%, #67c23a 100%);
  overflow: hidden;
}
.background-mask {
  position: absolute;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(2px);
  z-index: -1;
}
.app-container {
  min-height: 100vh;
  min-width: 100vw;
  position: relative;
  z-index: 1;
}
</style>
