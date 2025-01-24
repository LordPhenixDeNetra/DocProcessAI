# import cv2
# import numpy as np
# from skimage import filters
#
# class DocumentPreprocessor:
#     def __init__(self):
#         self.dpi = 300
#
#     def enhance_quality(self, image):
#         # Redimensionnement pour une résolution optimale
#         height, width = image.shape[:2]
#         target_height = int(height * self.dpi / 72)
#         target_width = int(width * self.dpi / 72)
#         image = cv2.resize(image, (target_width, target_height),
#                            interpolation=cv2.INTER_CUBIC)
#
#         # Correction de perspective
#         image = self._correct_skew(image)
#
#         # Amélioration du contraste
#         image = self._enhance_contrast(image)
#
#         return image
#
#     def _correct_skew(self, image):
#         # Détection des bords
#         edges = cv2.Canny(image, 50, 150, apertureSize=3)
#
#         # Détection des lignes
#         lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
#         if lines is not None:
#             # Calcul de l'angle de rotation
#             angle = np.median([line[0][1] for line in lines])
#             if angle > np.pi/4:
#                 angle = angle - np.pi/2
#
#             # Rotation de l'image
#             center = tuple(np.array(image.shape[1::-1]) / 2)
#             rot_mat = cv2.getRotationMatrix2D(center, angle * 180/np.pi, 1.0)
#             image = cv2.warpAffine(image, rot_mat, image.shape[1::-1],
#                                    flags=cv2.INTER_CUBIC)
#
#         return image
#
#     def _enhance_contrast(self, image):
#         # CLAHE (Contrast Limited Adaptive Histogram Equalization)
#         lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
#         l, a, b = cv2.split(lab)
#         clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
#         l = clahe.apply(l)
#         lab = cv2.merge((l,a,b))
#         return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)



import cv2
import numpy as np
from typing import Any

class DocumentProcessor:
    def __init__(self):
        self.supported_types = ['pdf', 'image', 'text', 'word']

    def preprocess(self, content: bytes, doc_type: str) -> Any:
        if doc_type not in self.supported_types:
            raise ValueError(f"Type de document non supporté: {doc_type}")

        if doc_type == 'image':
            return self._process_image(content)
        elif doc_type == 'pdf':
            return self._process_pdf(content)
        elif doc_type == 'word':
            return self._process_word(content)
        else:
            return self._process_text(content)

    def _process_image(self, content: bytes) -> np.ndarray:
        # Convertir les bytes en image
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Prétraitement
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)

        return enhanced

    def _process_pdf(self, content: bytes) -> bytes:
        # Pour l'instant, retourne le contenu tel quel
        # À améliorer selon les besoins
        return content

    def _process_word(self, content: bytes) -> bytes:
        # Pour l'instant, retourne le contenu tel quel
        # À améliorer selon les besoins
        return content

    def _process_text(self, content: str) -> str:
        # Nettoyage basique du texte
        text = content.strip()
        text = ' '.join(text.split())  # Normaliser les espaces
        return text