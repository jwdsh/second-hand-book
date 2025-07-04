import cv2
import numpy as np
import magic
from typing import Tuple, Optional


def validate_image_format(image_path: str) -> bool:
    """验证是否为支持的图片格式"""
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(image_path)
    return file_type.startswith('image/')


def preprocess_image(image_path: str) -> np.ndarray:
    """
    图像预处理：
    1. 转换为灰度图
    2. 自适应直方图均衡化
    3. 降噪
    """
    if not validate_image_format(image_path):
        raise ValueError("Unsupported image format")

    img = cv2.imread(image_path)
    if img is None:
        raise IOError("Failed to load image")

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE (对比度受限自适应直方图均衡化)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 非局部均值降噪
    denoised = cv2.fastNlMeansDenoising(enhanced, h=10)

    return denoised


def find_isbn_region(image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    定位可能的ISBN区域（条码区域）
    使用边缘检测和轮廓分析
    """
    # 边缘检测
    edges = cv2.Canny(image, 50, 150)

    # 膨胀操作连接边缘
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # 查找轮廓
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选可能的条码区域
    barcode_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(cnt)

        # 基于长宽比和面积筛选
        if 1.5 < aspect_ratio < 10 and area > 1000:
            barcode_contours.append((x, y, w, h))

    # 返回最大区域
    if barcode_contours:
        return max(barcode_contours, key=lambda r: r[2] * r[3])
    return None