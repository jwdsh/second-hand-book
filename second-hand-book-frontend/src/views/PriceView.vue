<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const isbn = route.query.isbn as string

const prices = ref([
  { platform: '当当', price: 30 },
  { platform: '孔夫子', price: 28 },
  { platform: '京东', price: 32 },
])
const suggestPrice = ref(30)
const conditionImage = ref<File | null>(null)
const imageUrl = ref<string | null>(null)
const hasCondition = ref(false)
const conditionScore = ref<number | null>(null)

function handleCondition() {
  if (!conditionImage.value) {
    ElMessage.warning('请先上传书本图片')
    return
  }
  // 这里调用品相分析API，分析图片
  // 假设分析结果为85分
  conditionScore.value = 85
  hasCondition.value = true
  ElMessage.success('品相分析完成，评分：85')
}

function nextStep() {
  router.push({ name: 'final', query: { isbn, hasCondition: String(hasCondition.value) } })
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
