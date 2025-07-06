// API配置
export const API_BASE_URL = 'http://localhost:8000'

// API端点
export const API_ENDPOINTS = {
  EVALUATE: `${API_BASE_URL}/evaluate`,
  RECORDS: `${API_BASE_URL}/records`
}

// 调试配置
export const DEBUG_CONFIG = {
  enabled: true, // 开启/关闭调试模式
  logAPI: true,  // 记录API调用
  logData: true, // 记录数据处理
  logError: true // 记录错误信息
}

// 调试工具函数
export const debugLog = (category: string, message: string, data?: any) => {
  if (!DEBUG_CONFIG.enabled) return
  
  const emoji = {
    'API': '📡',
    'Data': '📊', 
    'Error': '❌',
    'Success': '✅',
    'Warning': '⚠️',
    'Info': 'ℹ️'
  }[category] || '🔍'
  
  console.log(`${emoji} [${category} Debug] ${message}`)
  if (data) {
    console.log('   数据详情:', data)
  }
}
