from fastapi import UploadFile
import numpy as np
import cv2
from paddleocr import PaddleOCR
import re

# Initialize PaddleOCR globally to ensure it's loaded only once.
# Using use_textline_orientation for better text orientation detection.
# 'lang' is set to 'en' (English) because ISBNs are primarily numeric/alphanumeric.
ocr_isbn_reader_instance = PaddleOCR(use_textline_orientation=True, lang='en')


class ISBNReader:
    @staticmethod
    async def read_from_image(file: UploadFile) -> str:
        """
        Performs OCR on an uploaded image to extract the ISBN.
        """
        try:
            contents = await file.read()
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                print("Error: Could not decode image from uploaded file. Please ensure it's a valid image file.")
                return ""

            # Perform OCR. This version of PaddleOCR seems to return a list
            # where the first element is a dictionary containing results.
            raw_ocr_output = ocr_isbn_reader_instance.ocr(img)

            potential_isbns = []

            isbn_pattern = re.compile(
                r'(?:ISBN(?:-1[03])?[:\s]*)?'
                r'('
                r'(?:97[89][-\s]?[0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,6}[-\s]?[0-9X])|'
                r'([0-9]{13})|'
                r'([0-9]{9}[0-9X])|'
                r'([0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,6}[-\s]?[0-9X])'
                r')'
                , re.IGNORECASE
            )

            # Now, get the actual recognized text lines for processing
            # Safely access the results, assuming raw_ocr_output is a list with a dict at index 0
            if isinstance(raw_ocr_output, list) and raw_ocr_output and isinstance(raw_ocr_output[0], dict):
                recognized_texts_list = raw_ocr_output[0].get('rec_texts', [])

                for text in recognized_texts_list:
                    if isinstance(text, str) and text.strip():  # Ensure text is a non-empty string
                        matches = isbn_pattern.findall(text)
                        if matches:
                            for match_group in matches:
                                for candidate_isbn in match_group:
                                    if candidate_isbn:
                                        cleaned_candidate = candidate_isbn.strip().replace(' ', '').replace(':',
                                                                                                            '').replace(
                                            '-', '')
                                        potential_isbns.append(cleaned_candidate)
                                        break  # Found a match in this group, move to next match_group

            for isbn_candidate in potential_isbns:
                if ISBNReader.validate_isbn(isbn_candidate):
                    print(f"Validated ISBN found: {isbn_candidate}")
                    return isbn_candidate

            print("No valid ISBN found in the image after OCR and pattern matching.")
            return ""

        except Exception as e:
            print(f"Error during ISBN OCR process in read_from_image: {e}")
            return ""

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """
        Validates the ISBN string (implements basic ISBN-10 and ISBN-13 checksum validation).
        """
        cleaned_isbn = re.sub(r'[^0-9X]', '', isbn.upper())

        if len(cleaned_isbn) == 10:
            if not re.match(r'^\d{9}[\dX]$', cleaned_isbn):
                return False

            total_sum = 0
            for i in range(9):
                total_sum += int(cleaned_isbn[i]) * (10 - i)

            last_char = cleaned_isbn[9]
            if last_char == 'X':
                total_sum += 10
            else:
                total_sum += int(last_char)

            return total_sum % 11 == 0

        elif len(cleaned_isbn) == 13:
            if not cleaned_isbn.isdigit():
                return False

            total_sum = 0
            for i, digit_char in enumerate(cleaned_isbn):
                digit = int(digit_char)
                if i % 2 == 0:
                    total_sum += digit
                else:
                    total_sum += digit * 3

            return total_sum % 10 == 0
        else:
            return False
