<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElLoading } from 'element-plus'
import { API_ENDPOINTS } from '@/config/api'

const router = useRouter()
const isbn = ref('')
const image = ref<File | null>(null)
const imageUrl = ref<string | null>(null)
const loading = ref(false)

async function handleOcr() {
  if (!isbn.value && !image.value) {
    ElMessage.warning('请填写ISBN/书名或上传图片')
    return
  }
  
  loading.value = true
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在识别并估价...',
    background: 'rgba(0, 0, 0, 0.7)'
  })

  try {
    console.log('🚀 [OCR Debug] 开始完整评估流程')
    console.log('📋 [OCR Debug] 输入参数:', { 
      hasISBN: !!isbn.value, 
      hasImage: !!image.value,
      imageName: image.value?.name,
      note: '后端只支持当当网价格获取'
    })
    
    // 调用后端评估接口
    const formData = new FormData()
    if (image.value) {
      formData.append('file', image.value)
      console.log('� [OCR Debug] 已添加图片文件')
    }
    if (isbn.value) {
      formData.append('isbn', isbn.value)
      console.log('📖 [OCR Debug] 已添加ISBN:', isbn.value)
    }

    console.log('📡 [OCR Debug] 发送请求到:', API_ENDPOINTS.EVALUATE)
    const response = await fetch(API_ENDPOINTS.EVALUATE, {
      method: 'POST',
      body: formData
    })

    console.log('� [OCR Debug] 收到响应状态:', response.status)
    const result = await response.json()
    console.log('📊 [OCR Debug] 后端返回完整数据:', JSON.stringify(result, null, 2))

    if (result.error) {
      console.error('❌ [OCR Debug] 后端返回错误:', result.error)
      ElMessage.error(result.error)
      return
    }

    // 将结果存储到 sessionStorage，供后续页面使用
    console.log('💾 [OCR Debug] 保存评估结果到sessionStorage')
    sessionStorage.setItem('evaluationResult', JSON.stringify(result))
    
    // 直接跳转到最终结果页面，因为后端已经完成了完整的评估
    console.log('🔄 [OCR Debug] 跳转到最终结果页面')
    router.push({ name: 'final' })
    
    ElMessage.success('评估完成！')
  } catch (error) {
    console.error('💥 [OCR Debug] 评估失败:', error)
    ElMessage.error('评估失败，请检查网络连接或稍后重试')
  } finally {
    loading.value = false
    loadingInstance.close()
  }
}

function handleUpload(file: File) {
  image.value = file
  imageUrl.value = URL.createObjectURL(file)
}
</script>

<template>
  <el-card class="modern-card">
    <div class="step-bar">
      <div class="step active">
        <el-icon><document /></el-icon>
        <span>图书评估</span>
      </div>
      <div class="step">
        <el-icon><medal /></el-icon>
        <span>评估结果</span>
      </div>
    </div>
    <div class="content-row">
      <div class="upload-area">
        <div class="upload-title">上传书籍封面</div>
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
          <el-button class="modern-upload-btn" type="primary">上传图片</el-button>
        </el-upload>
        <el-image v-if="imageUrl" :src="imageUrl" class="preview-img" fit="cover" />
        <div class="upload-tip">支持jpg/png，建议正面封面</div>
      </div>
      <div class="divider"></div>
      <div class="input-area">
        <div class="input-title">输入ISBN</div>
        <el-input v-model="isbn" placeholder="请输入ISBN或书名" clearable class="modern-input" />
        <div class="input-tip">可手动输入或扫描图片自动识别</div>
      </div>
    </div>
    <el-button type="success" @click="handleOcr" class="modern-submit-btn" :loading="loading">
      {{ loading ? '评估中...' : '开始评估' }}
    </el-button>
    <el-button class="history-btn-float-in-card" type="info" plain @click="router.push({ name: 'history' })">
      历史定价
    </el-button>
  </el-card>
</template>

<script lang="ts">
import { Document, Medal } from '@element-plus/icons-vue'
export default {
  components: { document: Document, medal: Medal },
}
</script>

<style scoped>
.modern-card {
  max-width: 720px;
  margin: 80px auto;
  border-radius: 22px;
  box-shadow:
    0 8px 32px 0 rgba(64, 158, 255, 0.1),
    0 1.5px 6px 0 rgba(103, 194, 58, 0.08);
  border: none;
  padding: 36px 38px 32px 38px;
  background: rgba(255, 255, 255, 0.98);
  transition: box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  gap: 32px;
  position: relative; /* 关键：为绝对定位按钮提供参照 */
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
.content-row {
  display: flex;
  align-items: flex-start;
  gap: 32px;
}
.upload-area,
.input-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload-title,
.input-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #222;
}
.modern-upload-btn {
  border-radius: 8px;
  font-weight: 600;
  margin-bottom: 12px;
}
.preview-img {
  width: 90px;
  height: 120px;
  border-radius: 10px;
  margin-bottom: 8px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.13);
}
.upload-tip,
.input-tip {
  font-size: 0.95rem;
  color: #b1b1b1;
  margin-top: 4px;
}
.divider {
  width: 1.5px;
  background: linear-gradient(180deg, #409eff 0%, #67c23a 100%);
  height: 120px;
  border-radius: 2px;
  margin: 0 18px;
}
.input-area {
  align-items: stretch;
}
.modern-input :deep(.el-input__inner) {
  border-radius: 8px;
  font-size: 1.08rem;
  padding: 10px 14px;
  transition: border-color 0.2s;
}
.modern-input :deep(.el-input__inner):focus {
  border-color: #67c23a;
  box-shadow: 0 0 0 2px rgba(103, 194, 58, 0.08);
}
.modern-submit-btn {
  border-radius: 10px;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 0 auto;
  margin-top: 18px;
  width: 60%;
  background: linear-gradient(90deg, #67c23a 0%, #409eff 100%);
  border: none;
  transition:
    box-shadow 0.2s,
    background 0.2s;
  box-shadow: 0 2px 8px 0 rgba(103, 194, 58, 0.08);
  display: block;
}
.modern-submit-btn:hover {
  background: linear-gradient(90deg, #409eff 0%, #67c23a 100%);
  color: #fff;
}
.history-btn {
  margin: 18px auto 0 auto;
  display: block;
  width: 60%;
  border-radius: 10px;
  font-size: 1.08rem;
  font-weight: 600;
  letter-spacing: 1px;
  background: #f6f8fa;
  color: #409eff;
  border: 1.5px solid #dbeafe;
  transition:
    background 0.2s,
    color 0.2s;
}
.history-btn:hover {
  background: #e8f3ff;
  color: #67c23a;
  border-color: #67c23a;
}
.history-btn-float-in-card {
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
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.1);
  padding: 12px 28px;
  transition:
    background 0.2s,
    color 0.2s,
    box-shadow 0.2s;
}
.history-btn-float-in-card:hover {
  background: #e8f3ff;
  color: #67c23a;
  border-color: #67c23a;
  box-shadow: 0 8px 32px rgba(103, 194, 58, 0.13);
}
</style>
