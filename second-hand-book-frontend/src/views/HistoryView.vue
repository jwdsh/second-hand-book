<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Delete, PriceTag, Star, Collection } from '@element-plus/icons-vue'
import BackButton from '@/components/BackButton.vue'

interface PriceHistoryItem {
  time: string
  isbn: string
  conditionScore?: number
  price: number
  suggestPrice: number
  platforms: { platform: string; price: number }[]
}

const history = ref<PriceHistoryItem[]>([])

function loadHistory() {
  console.log('📚 [History Debug] 开始加载历史记录')
  
  // 只从浏览器本地存储获取历史记录
  const rawData = sessionStorage.getItem('priceHistory') || '[]'
  console.log('💾 [History Debug] 从sessionStorage读取的原始数据:', rawData)
  
  history.value = JSON.parse(rawData)
  console.log('📊 [History Debug] 解析后的历史记录:', JSON.stringify(history.value, null, 2))
  console.log('📈 [History Debug] 历史记录数量:', history.value.length)
}

function handleClear() {
  ElMessageBox.confirm('确定要清空所有历史定价记录吗？', '提示', {
    confirmButtonText: '清空',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    sessionStorage.removeItem('priceHistory')
    loadHistory()
    ElMessage.success('历史记录已清空')
  })
}

onMounted(loadHistory)
</script>

<template>
  <el-card class="history-card">
    <div class="history-header">
      <div class="history-title">
        <el-icon style="font-size: 1.6rem; color: #409eff; margin-right: 8px"><Collection /></el-icon>
        历史定价记录
      </div>
      <el-button type="danger" :icon="Delete" @click="handleClear" size="small" plain>清空历史</el-button>
    </div>
    <el-table
      :data="history"
      class="modern-table"
      v-if="history.length"
      stripe
      style="width: 100%; border-radius: 14px; overflow: hidden"
    >
      <el-table-column label="时间" width="160">
        <template #default="scope">
          <span>{{ scope.row.time }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="isbn" label="ISBN" width="120" />
      <el-table-column label="品相分" width="90">
        <template #default="scope">
          <el-tag v-if="scope.row.conditionScore !== undefined" type="success" effect="plain">
            <el-icon style="vertical-align: middle; margin-right: 2px"><Star /></el-icon>
            {{ scope.row.conditionScore }}
          </el-tag>
          <span v-else style="color: #bbb">--</span>
        </template>
      </el-table-column>
      <el-table-column label="建议价" width="100">
        <template #default="scope">
          <el-tag type="info" effect="plain">
            <el-icon style="vertical-align: middle; margin-right: 2px"><PriceTag /></el-icon>
            ￥{{ scope.row.suggestPrice }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="最终价" width="100">
        <template #default="scope">
          <el-tag type="success"> ￥{{ scope.row.price }} </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="平台价格">
        <template #default="scope">
          <div class="platforms">
            <el-tag
              v-for="p in scope.row.platforms"
              :key="p.platform"
              size="small"
              effect="plain"
              style="margin-right: 6px; margin-bottom: 2px"
            >
              {{ p.platform }}: ￥{{ p.price }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div v-else class="empty-tip">
      <el-icon style="font-size: 2.2rem; color: #bfcbd9; margin-bottom: 8px"><Collection /></el-icon>
      暂无历史定价记录
    </div>
    <BackButton />
  </el-card>
</template>

<style scoped>
.history-card {
  max-width: 900px;
  margin: 60px auto 0 auto;
  border-radius: 22px;
  box-shadow:
    0 8px 32px 0 rgba(64, 158, 255, 0.1),
    0 1.5px 6px 0 rgba(103, 194, 58, 0.08);
  border: none;
  padding: 38px 38px 28px 38px;
  background: rgba(255, 255, 255, 0.98);
  transition: box-shadow 0.3s;
  position: relative;
}
.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}
.history-title {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
}
.modern-table :deep(.el-table__header th) {
  background: #f6f8fa;
  font-weight: 700;
  font-size: 1.08rem;
  color: #222;
  border-bottom: none;
}
.modern-table :deep(.el-table__body td) {
  font-size: 1.08rem;
  border-bottom: 1px solid #f0f0f0;
}
.modern-table :deep(.el-table__row:last-child td) {
  border-bottom: none;
}
.platforms {
  display: flex;
  flex-wrap: wrap;
  gap: 2px 0;
}
.empty-tip {
  text-align: center;
  color: #bbb;
  font-size: 1.1rem;
  padding: 60px 0 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
