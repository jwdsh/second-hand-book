<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()
const evaluationData = ref<any>(null)
const finalPrice = ref(0)
const conditionScore = ref<number | null>(null)
const isbn = ref('')
const prices = ref<any>({})
const hasCondition = ref(false)

// 从 sessionStorage 加载评估结果
onMounted(() => {
  console.log('🏁 [Final Debug] 最终结果页面加载')
  
  const storedData = sessionStorage.getItem('evaluationResult')
  console.log('💾 [Final Debug] 从sessionStorage读取的原始数据:', storedData)
  
  if (storedData) {
    evaluationData.value = JSON.parse(storedData)
    console.log('📊 [Final Debug] 解析后的评估数据:', JSON.stringify(evaluationData.value, null, 2))
    
    // 直接使用后端返回的数据
    finalPrice.value = evaluationData.value.final_price
    isbn.value = evaluationData.value.isbn
    prices.value = evaluationData.value.prices
    
    // 处理品相评分（后端返回的是0-1之间的小数）
    if (evaluationData.value.condition_score !== undefined && evaluationData.value.condition_score !== 0.9) {
      // 如果不是默认的0.9，说明有真实的品相分析
      conditionScore.value = Math.round(evaluationData.value.condition_score * 100)
      hasCondition.value = true
      console.log('⭐ [Final Debug] 品相评分处理:', {
        original: evaluationData.value.condition_score,
        converted: conditionScore.value,
        hasCondition: hasCondition.value
      })
    } else {
      // 使用默认评分或无品相分析
      hasCondition.value = false
      console.log('📝 [Final Debug] 使用默认品相评分，无实际分析')
    }
    
    console.log('📈 [Final Debug] 最终显示数据:', {
      isbn: isbn.value,
      finalPrice: finalPrice.value,
      conditionScore: conditionScore.value,
      hasCondition: hasCondition.value,
      prices: prices.value
    })
    
    // 保存到历史记录
    saveToHistory()
  } else {
    console.warn('⚠️ [Final Debug] 未找到评估数据，可能是直接访问该页面')
  }
})

// 保存定价结果到历史记录
function saveToHistory() {
  if (!evaluationData.value) {
    console.warn('⚠️ [History Debug] 没有评估数据，跳过历史记录保存')
    return
  }
  
  console.log('📝 [History Debug] 开始保存历史记录')
  
  const history = JSON.parse(sessionStorage.getItem('priceHistory') || '[]')
  console.log('📜 [History Debug] 当前历史记录数量:', history.length)
  
  const item = {
    time: new Date().toLocaleString(),
    isbn: evaluationData.value.isbn,
    conditionScore: hasCondition.value ? conditionScore.value : undefined,
    price: evaluationData.value.final_price,
    suggestPrice: evaluationData.value.final_price,
    platforms: Object.entries(evaluationData.value.prices).map(([platform, price]) => ({
      platform,
      price: price as number
    }))
  }
  
  console.log('💾 [History Debug] 准备保存的记录项:', JSON.stringify(item, null, 2))
  
  // 避免重复保存
  if (!history.length || JSON.stringify(history[0]) !== JSON.stringify(item)) {
    history.unshift(item)
    sessionStorage.setItem('priceHistory', JSON.stringify(history))
    console.log('✅ [History Debug] 历史记录已保存，新的记录数量:', history.length)
  } else {
    console.log('🔄 [History Debug] 记录重复，跳过保存')
  }
}
</script>

<template>
  <el-card class="final-card">
    <!-- 步骤条 -->
    <div class="step-bar">
      <div class="step done">
        <el-icon><document /></el-icon>
        <span>图书评估</span>
      </div>
      <div class="step active">
        <el-icon><medal /></el-icon>
        <span>评估结果</span>
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
          <div class="divider" v-if="hasCondition"></div>
          <div class="final-price-area">
            <div class="final-label">最终价格</div>
            <div class="final-value">￥{{ finalPrice }}</div>
          </div>
        </div>
      </el-card>
      
      <!-- 显示当当网参考价格 -->
      <el-card class="reference-price-card" shadow="never" v-if="Object.keys(prices).length">
        <div v-for="(price, platform) in prices" :key="platform" class="reference-item">
          <span class="platform-text">当当网参考价格  </span>
          <span class="platform-price">￥{{ price }}</span>
        </div>
      </el-card>
      <div class="desc-tip">
        <el-icon color="#67c23a" style="vertical-align: middle"><Check /></el-icon>
        <span>{{ hasCondition ? '已结合品相评分，定价更精准' : '基于市场平均价格计算' }}</span>
      </div>
    </div>
    <el-button class="back-btn" type="primary" @click="router.push('/')">返回首页</el-button>
  </el-card>
</template>

<script lang="ts">
import { Document, Medal, Check } from '@element-plus/icons-vue'
export default {
  components: { document: Document, medal: Medal, Check },
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
.platforms-card {
  border-radius: 16px;
  border: 1px solid #eef2f8;
  margin-top: 16px;
}
.platforms-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 12px;
  text-align: center;
}
.platforms-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}
.platform-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}
.platform-name {
  font-size: 0.9rem;
  color: #666;
}
.platform-price {
  font-size: 0.9rem;
  font-weight: 600;
  color: #409eff;
}

/* 参考价格卡片样式 */
.reference-price-card {
  border-radius: 16px;
  border: none;
  margin-top: 20px;
  background: #fafdff;
  box-shadow: 0 2px 8px 0 rgba(64, 158, 255, 0.06);
  border: 1px solid rgba(64, 158, 255, 0.1);
}

.reference-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
}

.platform-text {
  font-size: 1.1rem;
  color: #888;
  font-weight: 500;
}

.platform-price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #409eff;
  letter-spacing: 1px;
}
</style>
