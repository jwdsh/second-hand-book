<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const hasCondition = route.query.hasCondition === 'true'
const finalPrice = hasCondition ? 27 : 30 // 示例：有品相评分则打折
const conditionScore = hasCondition ? 85 : null

// 保存定价结果到 sessionStorage
onMounted(() => {
  const history = JSON.parse(sessionStorage.getItem('priceHistory') || '[]')
  const item = {
    time: new Date().toLocaleString(),
    isbn: route.query.isbn || '',
    conditionScore: hasCondition ? conditionScore : undefined,
    price: finalPrice,
    suggestPrice: Number(route.query.suggestPrice) || finalPrice,
    platforms: JSON.parse(sessionStorage.getItem('lastPlatforms') || '[]'),
  }
  // 避免重复保存（如刷新页面），只保存与上一条不同的记录
  if (!history.length || JSON.stringify(history[0]) !== JSON.stringify(item)) {
    history.unshift(item)
    sessionStorage.setItem('priceHistory', JSON.stringify(history))
  }
})
</script>

<template>
  <el-card class="final-card">
    <!-- 步骤条 -->
    <div class="step-bar">
      <div class="step done">
        <el-icon><document /></el-icon>
        <span>识别书籍</span>
      </div>
      <div class="step done">
        <el-icon><coin /></el-icon>
        <span>查询价格</span>
      </div>
      <div class="step active">
        <el-icon><medal /></el-icon>
        <span>定价结果</span>
      </div>
    </div>
    <!-- 结果区 -->
    <div class="result-area">
      <div class="result-title">
        <el-icon color="#67c23a" style="font-size: 2.6rem"><medal /></el-icon>
        <span>最终定价结果</span>
      </div>
      <el-card class="price-main-card" shadow="never">
        <div class="price-main-content">
          <div class="score-area" v-if="hasCondition">
            <div class="score-label">品相评分</div>
            <div class="score-value">{{ conditionScore }}</div>
          </div>
          <div class="divider"></div>
          <div class="final-price-area">
            <div class="final-label">最终价格</div>
            <div class="final-value">￥{{ finalPrice }}</div>
          </div>
        </div>
      </el-card>
      <div class="desc-tip">
        <el-icon color="#67c23a" style="vertical-align: middle"><Check /></el-icon>
        <span>{{ hasCondition ? '已结合品相评分，定价更精准' : '未结合品相评分，建议上传图片获得更精准定价' }}</span>
      </div>
    </div>
    <el-button class="back-btn" type="primary" @click="router.push('/')">返回首页</el-button>
  </el-card>
</template>

<script lang="ts">
import { Document, Coin, Medal, Check } from '@element-plus/icons-vue'
export default {
  components: { document: Document, coin: Coin, medal: Medal, Check },
}
</script>

<style scoped>
.final-card {
  max-width: 600px;
  margin: 80px auto;
  border-radius: 22px;
  box-shadow:
    0 8px 32px 0 rgba(64, 158, 255, 0.1),
    0 1.5px 6px 0 rgba(103, 194, 58, 0.08);
  border: none;
  background: rgba(255, 255, 255, 0.98);
  padding: 38px 38px 32px 38px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.step-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding: 0 10px;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #bfcbd9;
  font-size: 1.05rem;
  gap: 4px;
  transition: color 0.2s;
}
.step.done,
.step.active {
  color: #409eff;
  font-weight: 700;
}
.step.active {
  color: #67c23a;
}
.step .el-icon {
  font-size: 2rem;
}
.result-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}
.result-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 8px;
  letter-spacing: 1px;
}
.price-main-card {
  width: 100%;
  border-radius: 16px;
  background: #fafdff;
  box-shadow: 0 2px 8px 0 rgba(64, 158, 255, 0.04);
  padding: 0;
}
.price-main-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  min-height: 110px;
}
.score-area {
  flex: 1;
  text-align: center;
  padding: 24px 0;
}
.score-label {
  font-size: 1.08rem;
  color: #888;
  margin-bottom: 6px;
}
.score-value {
  font-size: 2.1rem;
  color: #409eff;
  font-weight: 800;
  letter-spacing: 2px;
}
.divider {
  width: 1.5px;
  height: 60px;
  background: linear-gradient(180deg, #409eff 0%, #67c23a 100%);
  border-radius: 2px;
  margin: 0 24px;
}
.final-price-area {
  flex: 1;
  text-align: center;
  padding: 24px 0;
}
.final-label {
  font-size: 1.13rem;
  color: #888;
  margin-bottom: 6px;
}
.final-value {
  font-size: 2.4rem;
  color: #67c23a;
  font-weight: 900;
  letter-spacing: 2px;
}
.desc-tip {
  margin-top: 8px;
  color: #67c23a;
  font-size: 1.08rem;
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
}
.back-btn {
  width: 100%;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin-top: 8px;
  background: linear-gradient(90deg, #409eff 0%, #67c23a 100%);
  border: none;
  transition:
    background 0.2s,
    box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(103, 194, 58, 0.08);
}
.back-btn:hover {
  background: linear-gradient(90deg, #67c23a 0%, #409eff 100%);
  color: #fff;
}
</style>
