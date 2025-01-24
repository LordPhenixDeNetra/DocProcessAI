from .base_extractor import BaseExtractor
from pdf2image import convert_from_bytes
import pytesseract
import numpy as np

class PDFExtractor(BaseExtractor):
    def __init__(self):
        # Chemin vers Tesseract pour Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract(self, content: bytes) -> str:
        try:
            # Convertir PDF en images
            images = convert_from_bytes(content)
            text = ""

            for image in images:
                # Convertir l'image PIL en array numpy
                img_array = np.array(image)
                # Extraire le texte
                page_text = pytesseract.image_to_string(img_array, lang='fra+eng')
                text += page_text + "\n"
            print("Text:\n", text)
            print("========================================")
            print("Text:\n", self.clean_text(text))
            # return self.clean_text(text)
            return text

        except Exception as e:
            raise Exception(f"Erreur d'extraction PDF: {str(e)}")