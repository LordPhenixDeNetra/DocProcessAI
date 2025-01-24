import os
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from typing import Optional
import io
from pdf2image import convert_from_bytes

class CVExtractor:
    """
    Classe principale pour extraire le texte des CV dans différents formats
    """
    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png']
        # Spécifier le chemin vers Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract_text(self, content: bytes, filename: str) -> str:
        """
        Extrait le texte du CV selon son format
        """
        file_ext = self._get_file_extension(filename)

        if file_ext not in self.supported_formats:
            raise ValueError(f"Format non supporté: {file_ext}")

        if file_ext == '.pdf':
            return self._extract_from_pdf(content)
        else:
            return self._extract_from_image(content)

    def _get_file_extension(self, filename: str) -> str:
        """Récupère l'extension du fichier en minuscules"""
        return os.path.splitext(filename)[1].lower()

    def _extract_from_pdf(self, content: bytes) -> str:
        """Extrait le texte d'un PDF"""
        try:
            # Utiliser convert_from_bytes au lieu de convert_from_path
            images = convert_from_bytes(content)

            # Extraire le texte de chaque page
            full_text = []
            for image in images:
                # Convertir l'image PIL en array numpy
                img_array = np.array(image)
                # Extraire le texte de l'image
                text = self._process_image(img_array)
                full_text.append(text)

            return "\n".join(full_text)
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du PDF: {str(e)}")
    def _extract_from_image(self, content: bytes) -> str:
        """Extrait le texte d'une image"""
        try:
            # Convertir les bytes en image numpy
            nparr = np.frombuffer(content, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Traiter et extraire le texte
            return self._process_image(img)
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction de l'image: {str(e)}")

    def _process_image(self, image: np.ndarray) -> str:
        """Traite l'image pour améliorer l'extraction du texte"""
        try:
            # Convertir en niveaux de gris
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Débruiter l'image
            denoised = cv2.fastNlMeansDenoising(gray)

            # Améliorer le contraste
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)

            # Binarisation adaptative
            binary = cv2.adaptiveThreshold(
                enhanced,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

            # Extraire le texte avec Tesseract (français et anglais)
            text = pytesseract.image_to_string(binary, lang='fra+eng')

            # Nettoyer le texte
            text = self._clean_text(text)

            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur lors du traitement de l'image: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """Nettoie le texte extrait"""
        # Remplacer les multiples espaces par un seul
        text = ' '.join(text.split())

        # Remplacer les caractères problématiques
        text = text.replace('|', 'I')
        text = text.replace('¬', '-')

        # Supprimer les caractères non imprimables
        text = ''.join(char for char in text if char.isprintable())

        return text