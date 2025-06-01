import os
import base64
import requests
import json
import re
from typing import Tuple, List
from fastapi import UploadFile
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

# 获取新版百度API Key
QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")

class BookAnalyzer:
    @staticmethod
    async def analyze_book(images: List[UploadFile]) -> Tuple[str, float]:
        """
        使用新版千帆API分析图书封面（支持多张图片），返回书名和综合品相评分
        
        参数:
            images: 同一本书的多张图片列表（不同角度）
        
        返回格式: (书名, 综合评分)
        """
        try:
            # 1. 准备图片内容
            image_contents = []
            for image in images:
                contents = await image.read()
                image_base64 = base64.b64encode(contents).decode('utf-8')
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                })
            
            # 2. 构造专业提示词
            prompt = (
                "你是一名专业的图书评估专家。请根据提供的一张或多张图书照片（同一本书的不同角度）完成以下任务：\n\n"
                "1. 识别图书书名（中文书名使用《》标注，外文书名使用斜体）\n"
                "2. 综合评估图书品相，考虑以下因素：\n"
                "   - 封面/封底是否有破损、撕裂或折痕\n"
                "   - 页面是否有污渍、黄斑或涂写\n"
                "   - 书角是否有磨损或卷曲\n"
                "   - 书脊是否完好，有无开裂\n"
                "   - 整体老化程度\n\n"
                "请严格按照以下格式返回结果：\n"
                "书名：《书名》\n"
                "综合评分：0.85\n\n"
                "注意：\n"
                "- 评分保留3位小数\n"
                "- 基于所有照片给出综合评分\n"
                "- 不要包含任何其他文字或解释"

            )
            
            # 3. 构造API请求
            url = "https://qianfan.baidubce.com/v2/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {QIANFAN_API_KEY}" 
            }
            
            # 创建消息内容 - 文字提示 + 所有图片
            content = [{"type": "text", "text": prompt}]
            content.extend(image_contents)
            
            payload = {
                "model": "ernie-4.5-8k-preview",  
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "temperature": 0.1,  # 低温度值使输出更确定
                "max_tokens": 150     # 增加输出长度以包含书名和综合评分
            }
            
            # 4. 发送请求
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # 5. 处理响应
            if response.status_code == 200:
                result = response.json()
                #print("完整模型响应：", json.dumps(result, indent=2, ensure_ascii=False))
                reply = result["choices"][0]["message"]["content"]

                
                # 解析书名和评分
                book_title, score = BookAnalyzer.parse_response(reply)
                return book_title, score
            else:
                print(f"API请求失败: {response.status_code}, {response.text}")
                return "未知书名", 0.5
        
        except Exception as e:
            print(f"图书分析失败: {e}")
            return "未知书名", 0.5

    @staticmethod
    def parse_response(reply: str) -> Tuple[str, float]:
        #print(f"原始回复内容:\n{reply}\n{'='*50}")

        # 初始化默认值
        book_title = "未知书名"
        score = 0.5
        
        try:
            # 尝试提取书名
            title_match = re.search(r"书名[：:]\s*([《](.+?)[》]|(.+))", reply)
            if title_match:
        
                if title_match.group(2):
                    book_title = title_match.group(2)
    
                elif title_match.group(3):
                    book_title = title_match.group(3).strip()
            else:
       
                alt_match = re.search(r"《(.+?)》", reply)
                if alt_match:
                    book_title = alt_match.group(1)

            book_title = book_title.replace("《", "").replace("》", "").strip()
     
            score_match = re.search(r"(综合)?评分[：:]\s*(\d?\.\d{1,3})", reply)
            if score_match:
                score = float(score_match.group(2))
                # 确保评分在0-1之间
                if score < 0 or score > 1:
                    score = 0.5
            else:
  
                score_match_alt = re.search(r"\b0?\.\d{1,3}\b|\b1\.0{1,3}\b", reply)
                if score_match_alt:
                    score = float(score_match_alt.group())
                    if score < 0 or score > 1:
                        score = 0.5
                else:
                    print(f"未找到评分信息，使用默认值")
        except Exception as e:
            print(f"解析回复失败: {e}")
        
        return book_title, score
