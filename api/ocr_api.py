from fastapi import APIRouter, File, UploadFile
from modules.ocr_isbn.ocr_processor import process_image
import tempfile
import os

router = APIRouter()


@router.post("/ocr")
async def process_book_image(image: UploadFile = File(...)):
    """处理上传的书籍图片"""
    try:
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await image.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 处理图像
        result = process_image(tmp_path)

        # 清理临时文件
        os.unlink(tmp_path)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }