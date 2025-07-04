import os
import unittest
from modules.ocr_isbn.ocr_processor import process_image


class TestOCRProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建测试图片目录
        os.makedirs('tests/test_images', exist_ok=True)

    def test_valid_isbn(self):
        # 替换为你的实际测试图片路径
        result = process_image('tests/test_images/book_cover.jpg')
        self.assertIn('isbn', result)
        self.assertTrue(len(result['isbn']) in (10, 13))
        print(f"Detected ISBN: {result['isbn']}")
        print(f"Detected Title: {result.get('title', '')}")

    def test_no_text_image(self):
        # 纯色背景测试
        result = process_image('tests/test_images/blank.jpg')
        self.assertEqual(result['isbn'], '')
        self.assertEqual(result['title'], '')

    def test_invalid_image(self):
        with self.assertRaises(ValueError):
            process_image('tests/test_images/invalid.txt')

    def test_barcode_detection(self):
        # 条码图片测试
        result = process_image('tests/test_images/barcode_only.jpg')
        self.assertTrue(len(result['isbn']) in (10, 13))


if __name__ == '__main__':
    unittest.main()