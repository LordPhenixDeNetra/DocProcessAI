import pytest
from unittest.mock import Mock, patch
import os
import tempfile
from datetime import datetime

# Imports relatifs depuis la racine du projet
from ..preprocessing.document_processor import DocumentPreprocessor
from ..extraction.intelligent_extractor import IntelligentExtractor, ExtractedData
from ..validation.document_validator import DocumentValidator

class TestDocumentProcessing:
    @pytest.fixture
    def setup_test_files(self):
        """
        Fixture pytest qui crée des fichiers de test temporaires.
        Les fichiers sont automatiquement supprimés après chaque test.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Créer un PDF de test plus réaliste
            pdf_path = os.path.join(tmp_dir, "test.pdf")
            with open(pdf_path, "wb") as f:
                # Structure minimale d'un PDF valide
                pdf_content = (
                    b"%PDF-1.4\n"
                    b"1 0 obj\n"
                    b"<< /Type /Catalog /Pages 2 0 R >>\n"
                    b"endobj\n"
                    b"trailer\n"
                    b"<< /Root 1 0 R >>\n"
                    b"%%EOF"
                )
                f.write(pdf_content)

            # Créer une image JPEG de test
            img_path = os.path.join(tmp_dir, "test.jpg")
            with open(img_path, "wb") as f:
                # En-tête et fin JPEG minimaux
                jpeg_content = (
                    b"\xFF\xD8"  # SOI (Start of Image)
                    b"\xFF\xE0\x00\x10JFIF\x00\x01\x01"  # JFIF header
                    b"\xFF\xD9"  # EOI (End of Image)
                )
                f.write(jpeg_content)

            # Créer un fichier invalide pour les tests négatifs
            invalid_path = os.path.join(tmp_dir, "invalid.txt")
            with open(invalid_path, "wb") as f:
                f.write(b"Not a valid document")

            yield {
                "pdf": pdf_path,
                "image": img_path,
                "invalid": invalid_path
            }

    def test_document_preprocessing(self, setup_test_files):
        """Teste le prétraitement des documents"""
        processor = DocumentPreprocessor()

        # Test avec différents types de fichiers
        for file_type, file_path in setup_test_files.items():
            with open(file_path, "rb") as f:
                content = f.read()

                if file_type == "invalid":
                    # Vérifie que les fichiers invalides lèvent une exception
                    with pytest.raises(ValueError):
                        processor.enhance_quality(content)
                else:
                    # Vérifie le traitement des fichiers valides
                    result = processor.enhance_quality(content)
                    assert result is not None
                    # Vérifie que le résultat a la bonne forme
                    assert hasattr(result, 'shape')
                    assert len(result.shape) == 3  # Height, Width, Channels

    @patch('backend.extraction.intelligent_extractor.IntelligentExtractor')
    def test_data_extraction(self, mock_extractor):
        """Teste l'extraction de données avec un mock"""
        # Configure le mock
        mock_extractor.extract.return_value = ExtractedData(
            document_type="invoice",
            fields={
                "total": "100.00",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "invoice_number": "INV-2024-001"
            },
            confidence=0.95
        )

        extractor = IntelligentExtractor()

        # Test avec différents contenus
        test_contents = [
            "Facture avec montant total: 100.00€",
            "Document sans montant apparent",
            ""  # Test avec une chaîne vide
        ]

        for content in test_contents:
            result = extractor.extract(content)
            assert result is not None
            assert isinstance(result.confidence, float)
            assert 0 <= result.confidence <= 1
            assert isinstance(result.fields, dict)

    def test_validation(self, setup_test_files):
        """Teste la validation des documents"""
        validator = DocumentValidator()

        # Test pour chaque type de fichier
        for file_type, file_path in setup_test_files.items():
            with open(file_path, "rb") as f:
                content = f.read()
                result = validator.validate(content, os.path.basename(file_path))

                if file_type == "invalid":
                    assert not result.is_valid
                    assert len(result.errors) > 0
                else:
                    assert result.is_valid
                    assert len(result.errors) == 0

    @pytest.mark.parametrize("file_size", [
        1024,        # 1 KB
        1024*1024,   # 1 MB
        10*1024*1024 # 10 MB
    ])
    def test_file_size_limits(self, file_size):
        """Teste les limites de taille de fichier"""
        validator = DocumentValidator()

        # Créé un fichier de test de taille spécifique
        content = b"0" * file_size

        result = validator.validate(content, "test.pdf")

        # Vérifie si le résultat est conforme aux limites configurées
        if file_size > validator.max_file_size:
            assert not result.is_valid
            assert any("taille" in error.lower() for error in result.errors)
        else:
            assert result.is_valid or any("taille" not in error.lower() for error in result.errors)