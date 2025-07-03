import asyncio
import os
from pathlib import Path
from fastapi import UploadFile
from io import BytesIO
from analyzer import BookAnalyzer
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

class BookImageLoader:
    """用于从本地加载图书图片的工具类"""
    
    @staticmethod
    def load_images_from_folder(folder_path: str) -> list:
        """
        从指定文件夹加载所有图片文件
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"文件夹不存在: {folder_path}")
            
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        return [
            os.path.join(folder_path, f) 
            for f in os.listdir(folder_path) 
            if any(f.lower().endswith(ext) for ext in image_extensions)
        ]
    
    @staticmethod
    def create_upload_files(image_paths: list) -> list:
        """
        根据图片路径列表创建UploadFile对象列表
        """
        return [
            UploadFile(
                filename=os.path.basename(path),
                file=BytesIO(open(path, "rb").read())
            ) for path in image_paths
        ]

async def test_book_analysis(image_folder: str):
    """
    测试图书分析函数
    """
    print(f"\n开始测试图书分析: {image_folder}")
    
    try:
        # 1. 加载图片
        image_paths = BookImageLoader.load_images_from_folder(image_folder)
        if not image_paths:
            print("警告: 未找到图片文件")
            return
            
        print(f"找到 {len(image_paths)} 张图片")
            
        # 2. 创建UploadFile对象
        upload_files = BookImageLoader.create_upload_files(image_paths)
        
        # 3. 调用分析函数
        title, score = await BookAnalyzer.analyze_book(upload_files)
        
        # 4. 打印结果
        print("\n分析结果:")
        print(f"  书名: {title}")
        print(f"  综合品相评分: {score:.3f}")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    # 测试多本书
    test_folders = [
        #"test_books/book1",  # 替换为实际路径
        "test_books/book2"   # 替换为实际路径
        #"test_books/book3"
    ]
    
    for folder in test_folders:
        asyncio.run(test_book_analysis(folder))