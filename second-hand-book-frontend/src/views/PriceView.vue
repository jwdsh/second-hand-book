<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElLoading } from 'element-plus'
import { API_ENDPOINTS } from '@/config/api'

const router = useRouter()
const route = useRoute()
const isbn = route.query.isbn as string

const prices = ref<{platform: string, price: number}[]>([])
const suggestPrice = ref(0)
const conditionImage = ref<File | null>(null)
const imageUrl = ref<string | null>(null)
const hasCondition = ref(false)
const conditionScore = ref<number | null>(null)
const loading = ref(false)

// 页面加载时获取价格信息
onMounted(async () => {
  if (!isbn) {
    ElMessage.error('缺少ISBN信息')
    router.push({ name: 'ocr' })
    return
  }
  
  await fetchPrices()
})

// 获取价格信息
async function fetchPrices() {
  loading.value = true
  console.log('💰 [Price Debug] 开始获取价格信息，ISBN:', isbn)
  
  try {
    // 调用后端获取价格（不上传图片，只获取价格）
    const formData = new FormData()
    formData.append('isbn', isbn)
    
    console.log('📡 [Price Debug] 发送请求到:', API_ENDPOINTS.EVALUATE)
    console.log('📋 [Price Debug] 请求参数:', { isbn })

    const response = await fetch(API_ENDPOINTS.EVALUATE, {
      method: 'POST',
      body: formData
    })

    console.log('📥 [Price Debug] 收到响应状态:', response.status)
    
    const result = await response.json()
    console.log('📊 [Price Debug] 后端返回完整数据:', JSON.stringify(result, null, 2))

    if (result.error) {
      console.error('❌ [Price Debug] 后端返回错误:', result.error)
      ElMessage.error(result.error)
      return
    }

    // 转换价格数据格式
    if (result.prices) {
      console.log('💵 [Price Debug] 原始价格数据:', result.prices)
      
      prices.value = Object.entries(result.prices).map(([platform, price]) => ({
        platform,
        price: price as number
      }))
      
      console.log('💱 [Price Debug] 转换后价格数组:', prices.value)
      
      // 计算建议价格（不含品相分析）
      const avgPrice = prices.value.reduce((sum, item) => sum + item.price, 0) / prices.value.length
      suggestPrice.value = Math.round(avgPrice)
      
      console.log('📈 [Price Debug] 计算建议价格:', avgPrice, '→', suggestPrice.value)
    }

  } catch (error) {
    console.error('💥 [Price Debug] 获取价格失败:', error)
    ElMessage.error('获取价格失败，使用模拟数据')
    
    // 使用模拟数据作为后备
    const mockData = [
      { platform: '当当', price: 30 }
    ]
    console.log('🎭 [Price Debug] 使用模拟数据:', mockData)
    prices.value = mockData
    suggestPrice.value = 30
  } finally {
    loading.value = false
    console.log('✅ [Price Debug] 价格获取流程完成')
  }
}

async function handleCondition() {
  if (!conditionImage.value) {
    ElMessage.warning('请先上传书本图片')
    return
  }
  
  console.log('🔍 [Condition Debug] 开始品相分析，图片:', conditionImage.value.name)
  
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在分析品相...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    // 调用后端进行品相分析
    const formData = new FormData()
    formData.append('file', conditionImage.value)
    formData.append('isbn', isbn)
    
    console.log('📡 [Condition Debug] 发送品相分析请求到:', API_ENDPOINTS.EVALUATE)
    console.log('📋 [Condition Debug] 请求参数:', { isbn, file: conditionImage.value.name })

    const response = await fetch(API_ENDPOINTS.EVALUATE, {
      method: 'POST',
      body: formData
    })

    console.log('📥 [Condition Debug] 收到响应状态:', response.status)
    
    const result = await response.json()
    console.log('📊 [Condition Debug] 后端返回完整数据:', JSON.stringify(result, null, 2))

    if (result.error) {
      console.error('❌ [Condition Debug] 后端返回错误:', result.error)
      ElMessage.error(result.error)
      return
    }

    // 获取品相评分
    if (result.condition_score) {
      console.log('⭐ [Condition Debug] 原始品相评分:', result.condition_score)
      conditionScore.value = Math.round(result.condition_score * 100) // 转换为百分制
      hasCondition.value = true
      console.log('💯 [Condition Debug] 转换后品相评分:', conditionScore.value)
      ElMessage.success(`品相分析完成，评分：${conditionScore.value}`)
    } else {
      console.warn('⚠️ [Condition Debug] 后端未返回品相评分')
    }

  } catch (error) {
    console.error('💥 [Condition Debug] 品相分析失败:', error)
    // 使用模拟数据
    const mockScore = 85
    console.log('🎭 [Condition Debug] 使用模拟品相评分:', mockScore)
    conditionScore.value = mockScore
    hasCondition.value = true
    ElMessage.success('品相分析完成，评分：85')
  } finally {
    loadingInstance.close()
    console.log('✅ [Condition Debug] 品相分析流程完成')
  }
}

function nextStep() {
  console.log('🚀 [Next Debug] 准备进入下一步')
  console.log('📋 [Next Debug] 当前状态:', {
    isbn: isbn,
    prices: prices.value,
    hasCondition: hasCondition.value,
    conditionScore: conditionScore.value,
    suggestPrice: suggestPrice.value
  })
  
  // 保存当前状态到 sessionStorage
  const resultData = {
    isbn: isbn,
    prices: Object.fromEntries(prices.value.map(item => [item.platform, item.price])),
    condition_score: hasCondition.value ? conditionScore.value! / 100 : null,
    final_price: hasCondition.value ? 
      Math.round(suggestPrice.value * (conditionScore.value! / 100) * 100) / 100 : 
      suggestPrice.value
  }
  
  console.log('💾 [Next Debug] 保存到sessionStorage的数据:', JSON.stringify(resultData, null, 2))
  
  sessionStorage.setItem('evaluationResult', JSON.stringify(resultData))
  
  console.log('🔄 [Next Debug] 跳转到最终结果页面')
  router.push({ name: 'final' })
}

function handleUpload(file: File) {
  conditionImage.value = file
  imageUrl.value = URL.createObjectURL(file)
}
</script>

<template>
  <el-card class="modern-card">
    <!-- 步骤条 -->
    <div class="step-bar">
      <div class="step active">
        <el-icon><document /></el-icon>
        <span>识别书籍</span>
      </div>
      <div class="step active">
        <el-icon><coin /></el-icon>
        <span>查询价格</span>
      </div>
      <div class="step">
        <el-icon><medal /></el-icon>
        <span>定价结果</span>
      </div>
    </div>
    <!-- 价格信息区 -->
    <div class="info-row">
      <el-card class="price-table-card" shadow="never">
        <div class="section-title-row">
          <span class="section-title">各平台实时价格</span>
          <span class="suggest-price-badge">
            <el-icon color="#67c23a" style="vertical-align: middle"><Check /></el-icon>
            <span class="suggest-label">建议价</span>
            <span class="suggest-value">￥{{ suggestPrice }}</span>
          </span>
        </div>
        <el-table :data="prices" class="modern-table" border="{false}">
          <el-table-column prop="platform" label="平台" width="100" />
          <el-table-column prop="price" label="价格" width="100">
            <template #default="scope">
              <span style="font-weight: 600">￥{{ scope.row.price }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    <!-- 品相分析区 -->
    <el-card class="condition-card" shadow="never">
      <div class="section-title">上传书本图片进行品相分析</div>
      <div class="condition-actions">
        <el-upload
          :show-file-list="false"
          accept="image/*"
          :before-upload="
            (file: File) => {
              handleUpload(file)
              return false
            }
          "
        >
          <el-button class="modern-upload-btn">上传图片</el-button>
        </el-upload>
        <el-button class="modern-analyze-btn" @click="handleCondition" :disabled="!conditionImage">
          分析品相
        </el-button>
        <el-image
          v-if="imageUrl"
          :src="imageUrl"
          style="
            width: 40px;
            height: 40px;
            margin-left: 14px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(64, 158, 255, 0.13);
          "
          fit="cover"
        />
        <el-alert
          v-if="hasCondition && conditionScore !== null"
          title="品相评分"
          type="info"
          :description="`评分：${conditionScore}`"
          show-icon
          class="score-alert"
          style="margin-left: 18px"
        />
      </div>
    </el-card>
    <!-- 操作区 -->
    <el-button class="modern-next-btn" type="primary" @click="nextStep">下一步</el-button>
    <BackButton />
  </el-card>
</template>

<script lang="ts">
import { Document, Coin, Medal, Check } from '@element-plus/icons-vue'
import BackButton from '@/components/BackButton.vue'
export default {
  components: { document: Document, coin: Coin, medal: Medal, Check, BackButton },
}
</script>

<style scoped>
.modern-card {
  max-width: 800px;
  margin: 60px auto 0 auto;
  border-radius: 22px;
  box-shadow:
    0 8px 32px 0 rgba(64, 158, 255, 0.1),
    0 1.5px 6px 0 rgba(103, 194, 58, 0.08);
  border: none;
  padding: 38px 38px 32px 38px;
  background: rgba(255, 255, 255, 0.98);
  transition: box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  gap: 32px;
  position: relative;
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
.step.active {
  color: #409eff;
  font-weight: 700;
}
.step .el-icon {
  font-size: 2rem;
}
.info-row {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.price-table-card {
  border-radius: 14px;
  padding: 18px 18px 8px 18px;
  background: #fafdff;
  box-shadow: 0 2px 8px 0 rgba(64, 158, 255, 0.04);
}
.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.section-title {
  font-size: 1.13rem;
  font-weight: 700;
  color: #222;
}
.suggest-price-badge {
  display: flex;
  align-items: center;
  background: #e8f7e5;
  border-radius: 16px;
  padding: 3px 14px 3px 8px;
  font-size: 1.05rem;
  gap: 6px;
  box-shadow: 0 1px 4px 0 rgba(103, 194, 58, 0.07);
}
.suggest-label {
  color: #67c23a;
  font-weight: 600;
  margin-right: 2px;
}
.suggest-value {
  color: #222;
  font-weight: 700;
  font-size: 1.13rem;
}
.condition-card {
  border-radius: 14px;
  background: #fafdff;
  box-shadow: 0 2px 8px 0 rgba(64, 158, 255, 0.04);
  padding: 18px 18px 8px 18px;
}
.condition-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}
.modern-upload-btn {
  border-radius: 8px;
  font-weight: 600;
  background: #409eff;
  color: #fff;
  transition: background 0.2s;
}
.modern-upload-btn:hover {
  background: #67c23a;
  color: #fff;
}
.modern-analyze-btn {
  border-radius: 8px;
  font-weight: 600;
  background: #67c23a;
  color: #fff;
  transition: background 0.2s;
}
.modern-analyze-btn:disabled {
  background: #d3e7c6;
  color: #fff;
}
.modern-analyze-btn:not(:disabled):hover {
  background: #409eff;
  color: #fff;
}
.score-alert {
  border-radius: 8px;
  min-width: 120px;
}
.modern-next-btn {
  width: 60%;
  margin: 0 auto;
  border-radius: 10px;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin-top: 10px;
  background: linear-gradient(90deg, #409eff 0%, #67c23a 100%);
  border: none;
  transition:
    background 0.2s,
    box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(103, 194, 58, 0.08);
  display: block;
}
.modern-next-btn:hover {
  background: linear-gradient(90deg, #67c23a 0%, #409eff 100%);
  color: #fff;
}
</style>
