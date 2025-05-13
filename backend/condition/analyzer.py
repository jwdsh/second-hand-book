from fastapi import UploadFile
import numpy as np
import cv2

class ConditionAnalyzer:
    @staticmethod
    async def analyze_condition(file: UploadFile) -> float:
        """分析品相"""
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)/255 * 0.5 + 0.5