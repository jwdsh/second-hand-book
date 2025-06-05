<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const isbn = ref('')
const image = ref<File | null>(null)
const imageUrl = ref<string | null>(null)

function handleOcr() {
  if (!isbn.value && !image.value) {
    ElMessage.warning('请填写ISBN/书名或上传图片')
    return
  }
  // 这里调用OCR识别API，识别出ISBN或书名
  // 假设识别成功，跳转到价格页
  router.push({ name: 'price', query: { isbn: isbn.value } })
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
        <span>识别书籍信息</span>
      </div>
      <div class="step">
        <el-icon><coin /></el-icon>
        <span>查询价格</span>
      </div>
      <div class="step">
        <el-icon><medal /></el-icon>
        <span>定价结果</span>
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
        <div class="input-title">输入ISBN或书名</div>
        <el-input v-model="isbn" placeholder="请输入ISBN或书名" clearable class="modern-input" />
        <div class="input-tip">可手动输入或扫描图片自动识别</div>
      </div>
    </div>
    <el-button type="success" @click="handleOcr" class="modern-submit-btn">识别并查询价格</el-button>
    <el-button class="history-btn-float-in-card" type="info" plain @click="router.push({ name: 'history' })">
      历史定价
    </el-button>
  </el-card>
</template>

<script lang="ts">
import { Document, Coin, Medal } from '@element-plus/icons-vue'
export default {
  components: { document: Document, coin: Coin, medal: Medal },
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
