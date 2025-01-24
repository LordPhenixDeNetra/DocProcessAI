# api/endpoints/documents.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import List
import cv2
import numpy as np
from core.security import validate_api_key
from preprocessing.document_processor import DocumentProcessor
from validation.document_validator import DocumentValidator
from extraction.intelligent_extractor import IntelligentExtractor
from utils.logger import setup_logger

logger = setup_logger()
router = APIRouter()

# Initialisation des services
document_processor = DocumentProcessor()
document_validator = DocumentValidator()
document_extractor = IntelligentExtractor()

@router.post("/analyze")
async def analyze_document(
        file: UploadFile = File(...),
        api_key: str = Depends(validate_api_key)
):
    logger.info(f"Starting analysis of document: {file.filename}")
    logger.info(f"Content type: {file.content_type}")

    try:
        content = await file.read()
        logger.info(f"File size: {len(content)} bytes")

        # Validation initiale
        validation_result = document_validator.validate(content, file.filename)
        logger.info(f"Validation result: {validation_result}")

        if not validation_result.is_valid:
            logger.error(f"Validation failed: {validation_result.errors}")
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid document",
                    "errors": validation_result.errors,
                    "warnings": validation_result.warnings
                }
            )

        # Traitement différent selon le type de fichier
        if file.filename.lower().endswith('.pdf'):
            # TODO: Ajouter extraction de texte PDF
            # Pour l'instant, utilisons un texte exemple
            text = "Facture N° 2024-001\nDate: 18/01/2024\nTotal TTC: 100.00"
        else:
            # Traitement des images
            nparr = np.frombuffer(content, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise HTTPException(
                    status_code=400,
                    detail="Could not read image content"
                )

            # Prétraitement de l'image
            enhanced_image = document_processor.enhance_quality(image)
            # TODO: Ajouter OCR sur l'image améliorée
            text = "Contrat\nDate: 18/01/2024"  # À remplacer par OCR réel

        # Extraction des données
        extracted_data = document_extractor.extract(text)

        # Réponse
        return {
            "status": "success",
            "filename": file.filename,
            "document_type": extracted_data.document_type,
            "fields": extracted_data.fields,
            "confidence": extracted_data.confidence,
            "warnings": validation_result.warnings
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
    finally:
        await file.close()


# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from core.security import validate_api_key
# from preprocessing.document_processor import DocumentPreprocessor
# from validation.document_validator import DocumentValidator
# from extraction.intelligent_extractor import IntelligentExtractor
# import cv2
# import numpy as np
#
# router = APIRouter()
#
# # Initialisation des services
# document_processor = DocumentPreprocessor()
# document_validator = DocumentValidator()
# document_extractor = IntelligentExtractor()
#
# @router.post("/analyze")
# async def analyze_document(
#         file: UploadFile = File(...),
#         api_key: str = Depends(validate_api_key)
# ):
#     try:
#         # Lire le contenu du fichier
#         content = await file.read()
#
#         # Valider le document
#         validation_result = document_validator.validate(content, file.filename)
#         if not validation_result.is_valid:
#             raise HTTPException(
#                 status_code=400,
#                 detail={"errors": validation_result.errors}
#             )
#
#         # Convertir le contenu en image
#         nparr = np.frombuffer(content, np.uint8)
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#         # Prétraiter l'image
#         enhanced_image = document_processor.enhance_quality(image)
#
#         # Extraire le texte
#         text = "Exemple de texte extrait"  # À remplacer par l'extraction réelle
#
#         # Analyser le contenu
#         extracted_data = document_extractor.extract(text)
#
#         return {
#             "filename": file.filename,
#             "document_type": extracted_data.document_type,
#             "fields": extracted_data.fields,
#             "confidence": extracted_data.confidence,
#             "warnings": validation_result.warnings
#         }
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error processing document: {str(e)}"
#         )