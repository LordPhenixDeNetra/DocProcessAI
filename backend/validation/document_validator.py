# validation/document_validator.py
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class DocumentValidator:
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}

    def validate(self, file_content: bytes, filename: str) -> ValidationResult:
        errors = []
        warnings = []

        # Vérification de la taille
        if len(file_content) > self.max_file_size:
            errors.append("Le fichier dépasse la taille maximale autorisée")

        # Vérification de l'extension
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            errors.append(f"Extension de fichier non supportée: {file_ext}")

        # Vérification de l'intégrité
        if not self._check_file_integrity(file_content):
            errors.append("Le fichier semble corrompu")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_file_integrity(self, content: bytes) -> bool:
        try:
            # Vérification basique des signatures de fichiers
            if content.startswith(b'%PDF'):
                return self._validate_pdf(content)
            elif content.startswith(b'\xFF\xD8'):
                return self._validate_jpeg(content)
            elif content.startswith(b'\x89PNG\r\n'):
                return self._validate_png(content)
            return False
        except:
            return False

    def _validate_pdf(self, content: bytes) -> bool:
        return b'%PDF' in content and b'%%EOF' in content

    def _validate_jpeg(self, content: bytes) -> bool:
        return content.startswith(b'\xFF\xD8') and content.endswith(b'\xFF\xD9')

    def _validate_png(self, content: bytes) -> bool:
        return content.startswith(b'\x89PNG\r\n') and b'IEND' in content



















# from dataclasses import dataclass
# from typing import List, Optional
# import magic
# import hashlib
#
# @dataclass
# class ValidationResult:
#     is_valid: bool
#     errors: List[str]
#     warnings: List[str]
#
# class DocumentValidator:
#     def __init__(self):
#         self.max_file_size = 10 * 1024 * 1024  # 10MB
#         self.allowed_mime_types = [
#             'application/pdf',
#             'image/jpeg',
#             'image/png'
#         ]
#
#     def validate(self, file_content: bytes, filename: str) -> ValidationResult:
#         errors = []
#         warnings = []
#
#         # Vérification de la taille
#         if len(file_content) > self.max_file_size:
#             errors.append("Le fichier dépasse la taille maximale autorisée")
#
#         # Vérification du type MIME
#         mime_type = magic.from_buffer(file_content, mime=True)
#         if mime_type not in self.allowed_mime_types:
#             errors.append(f"Type de fichier non supporté: {mime_type}")
#
#         # Vérification de l'intégrité
#         if not self._check_file_integrity(file_content):
#             errors.append("Le fichier semble corrompu")
#
#         # Vérification du contenu suspect
#         suspicious_content = self._check_suspicious_content(file_content)
#         if suspicious_content:
#             warnings.extend(suspicious_content)
#
#         return ValidationResult(
#             is_valid=len(errors) == 0,
#             errors=errors,
#             warnings=warnings
#         )
#
#     def _check_file_integrity(self, content: bytes) -> bool:
#         try:
#             # Vérifications spécifiques selon le type de fichier
#             if content.startswith(b'%PDF'):
#                 return self._validate_pdf(content)
#             elif content.startswith(b'\xFF\xD8'):
#                 return self._validate_jpeg(content)
#             elif content.startswith(b'\x89PNG\r\n'):
#                 return self._validate_png(content)
#             return False
#         except:
#             return False
#
#     def _validate_pdf(self, content: bytes) -> bool:
#         # Vérification basique de la structure PDF
#         return b'%%EOF' in content
#
#     def _validate_jpeg(self, content: bytes) -> bool:
#         # Vérification des marqueurs JPEG
#         return content.endswith(b'\xFF\xD9')
#
#     def _validate_png(self, content: bytes) -> bool:
#         # Vérification de la signature PNG
#         return b'IEND' in content