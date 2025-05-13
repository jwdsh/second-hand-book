from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database.manager import DatabaseManager
from ocr.isbn_reader import ISBNReader
from crawler.price_crawler import PriceCrawler
from condition.analyzer import ConditionAnalyzer
from pricing.strategy import PricingStrategy

# 初始化FastAPI应用
app = FastAPI(title="图书估价系统", version="1.0.0")

# 配置跨域中间件（必须放在最前面）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库连接
db = DatabaseManager()

# ================== API路由区域 ==================
@app.post("/evaluate", summary="图书估价接口")
async def evaluate_book(
    file: UploadFile = File(None, description="上传图书照片"),
    isbn: str = Form(None, description="手动输入ISBN号")
):
    """核心估价接口，支持图片或ISBN输入"""
    try:
        # ISBN处理逻辑
        if not isbn and file:
            isbn = await ISBNReader.read_from_image(file)
        if not ISBNReader.validate_isbn(isbn):
            return {"error": "无效的ISBN号"}
        
        # 获取各平台价格
        prices = await PriceCrawler.fetch_prices(isbn)
        
        # 品相分析（有图片时执行）
        score = 0.9  # 默认品相分
        if file:
            score = await ConditionAnalyzer.analyze_condition(file)
        
        # 计算最终价格
        final_price = PricingStrategy.calculate_price(prices, score)
        
        # 存储记录
        record = {
            "isbn": isbn,
            "prices": prices,
            "score": score,
            "final_price": final_price
        }
        db.save_record(record)
        
        return {
            "isbn": isbn,
            "prices": prices,
            "condition_score": round(score, 2),
            "final_price": final_price
        }
    except Exception as e:
        return {"error": str(e), "detail": "请检查输入格式是否正确"}

@app.get("/records", summary="获取历史记录")
async def get_records(limit: int = 10):
    """获取最近评估记录"""
    try:
        records = db.get_records(limit)
        return [{
            "isbn": record["isbn"],
            "prices": eval(record["prices"]),
            "score": record["score"],
            "final_price": record["final_price"]
        } for record in records]
    except Exception as e:
        return {"error": str(e)}

# ================== 静态文件服务 ==================
app.mount(
    "/", 
    StaticFiles(directory="../frontend", html=True), 
    name="frontend"
)

# ================== 服务启动配置 ==================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,         # 开发时启用热重载
        access_log=False,    # 生产环境建议关闭访问日志
    )