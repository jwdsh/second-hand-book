const API_BASE = 'http://localhost:8000';

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    setupImagePreview();
});

// 图片预览功能
function setupImagePreview() {
    const input = document.getElementById('bookImage');
    const preview = document.querySelector('.preview');
    
    input.addEventListener('change', function(e) {
        preview.innerHTML = '';
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
}

// 表单提交处理
document.getElementById('evalForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);
    
    try {
        const formData = new FormData();
        const file = document.getElementById('bookImage').files[0];
        const isbn = document.getElementById('isbnInput').value.trim();

        if (file) formData.append('file', file);
        if (isbn) formData.append('isbn', isbn);

        const response = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('请求失败');
        const result = await response.json();

        if (result.error) {
            showError(result.error);
            return;
        }

        showResult(result);
        loadHistory();
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
});

// 显示结果
function showResult(data) {
    const content = `
        <div class="result-item">
            <div class="result-row">
                <span class="label">ISBN:</span>
                <span class="value">${data.isbn}</span>
            </div>
            <div class="result-row">
                <span class="label">品相评分:</span>
                <span class="value">${data.condition_score}</span>
            </div>
            <div class="price-comparison">
                <h4>平台价格对比</h4>
                <ul>
                    ${Object.entries(data.prices).map(([platform, price]) => `
                        <li>
                            <span class="platform">${platform}</span>
                            <span class="price">￥${price.toFixed(2)}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
            <div class="final-price">
                <h3>最终估价：￥${data.final_price.toFixed(2)}</h3>
            </div>
        </div>
    `;
    
    document.querySelector('.upload-section').classList.add('hidden');
    document.querySelector('.result-section').classList.remove('hidden');
    document.getElementById('resultContent').innerHTML = content;
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/records`);
        const records = await response.json();
        renderHistory(records);
    } catch (error) {
        console.error('加载历史记录失败:', error);
    }
}

function renderHistory(records) {
    const list = document.getElementById('historyList');
    list.innerHTML = records.map(record => `
        <li>
            <span class="isbn">${record.isbn}</span>
            <span class="score">评分: ${record.score.toFixed(2)}</span>
            <span class="price">￥${record.final_price.toFixed(2)}</span>
        </li>
    `).join('');
}

// 辅助功能
function showLoading(show) {
    const button = document.querySelector('button[type="submit"]');
    button.innerHTML = show ? '评估中...' : '开始评估';
}

function showError(message) {
    alert(`错误: ${message}`);
}