from .base_extractor import BaseExtractor
import cv2
import numpy as np
import pytesseract

class ImageExtractor(BaseExtractor):
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract(self, content: bytes) -> str:
        try:
            # Convertir bytes en image
            nparr = np.frombuffer(content, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Prétraitement
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray)

            # OCR
            text = pytesseract.image_to_string(denoised, lang='fra+eng')
            return self.clean_text(text)

        except Exception as e:
            raise Exception(f"Erreur d'extraction d'image: {str(e)}")