from paddleocr import PaddleOCR
from .image_utils import preprocess_image, find_isbn_region
from .isbn_utils import extract_isbn_from_text
import cv2
import logging
from typing import Dict, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ISBN-OCR")


class OCRProcessor:
    def __init__(self):
        """初始化OCR模型"""
        # 使用PP-OCRv3模型，开启方向分类器
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',
            rec_model_dir=None,
            cls_model_dir=None,
            use_gpu=False,  # 根据你的环境设置
            show_log=False
        )
        logger.info("OCR model initialized")

    def process_image(self, image_path: str) -> Dict[str, str]:
        """
        处理图像并返回识别结果
        返回: {'isbn': ISBN号, 'title': 书名}
        """
        try:
            # 图像预处理
            processed_img = preprocess_image(image_path)

            # 尝试定位ISBN区域
            region = find_isbn_region(processed_img)
            roi = None

            if region:
                x, y, w, h = region
                roi = processed_img[y:y + h, x:x + w]
                logger.info(f"Found potential ISBN region: {region}")
            else:
                roi = processed_img
                logger.warning("ISBN region not found, processing full image")

            # 执行OCR识别
            result = self.ocr.ocr(roi, cls=True)

            # 提取所有文本
            texts = []
            for line in result:
                if line and line[0]:
                    for word_info in line:
                        if word_info and word_info[1]:
                            texts.append(word_info[1][0])

            full_text = " ".join(texts)
            logger.info(f"OCR extracted text: {full_text[:100]}...")

            # 提取ISBN
            isbn = extract_isbn_from_text(full_text)

            # 尝试提取书名（简单启发式方法）
            title = self._extract_title(texts)

            return {
                'isbn': isbn,
                'title': title,
                'full_text': full_text
            }

        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            return {'error': str(e)}

    def _extract_title(self, texts: list) -> str:
        """
        从OCR结果中提取可能的书名
        启发式规则：最长文本行且不包含数字
        """
        if not texts:
            return ""

        # 过滤掉纯数字行
        candidate_lines = [t for t in texts if not t.replace(' ', '').isdigit()]

        if not candidate_lines:
            return ""

        # 选择最长的文本行
        title = max(candidate_lines, key=len)

        # 简单清理
        title = title.strip()
        if len(title) > 100:  # 书名通常不会过长
            return ""

        return title


# 单例模式
ocr_processor = OCRProcessor()


def process_image(image_path: str) -> Dict[str, str]:
    return ocr_processor.process_image(image_path)