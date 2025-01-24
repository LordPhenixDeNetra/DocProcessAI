# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_document_analysis():
    # Test avec un PDF valide
    with open("tests/test_files/facture_test.pdf", "rb") as f:
        response = client.post(
            "/documents/analyze",
            files={"file": ("facture_test.pdf", f, "application/pdf")},
            headers={"X-API-Key": "votre-clé-api-secrète"}
        )
        assert response.status_code == 200
        assert response.json()["document_type"] == "invoice"

    # Test avec une image valide
    with open("tests/test_files/contrat_test.jpg", "rb") as f:
        response = client.post(
            "/documents/analyze",
            files={"file": ("contrat_test.jpg", f, "image/jpeg")},
            headers={"X-API-Key": "votre-clé-api-secrète"}
        )
        assert response.status_code == 200
        assert response.json()["document_type"] == "contract"

    # Test avec un fichier invalide
    with open("tests/test_files/document_invalide.txt", "rb") as f:
        response = client.post(
            "/documents/analyze",
            files={"file": ("document_invalide.txt", f, "text/plain")},
            headers={"X-API-Key": "votre-clé-api-secrète"}
        )
        assert response.status_code == 400