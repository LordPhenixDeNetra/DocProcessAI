# api/endpoints/cv.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import Dict, Any
from core.security import validate_api_key
from extractors.cv_extractor import CVExtractor
from extractors.date_extractor import DateExtractor
# from extractors.section_extractor import CVSectionDetector
from processors.cv_processor import CVProcessor
from utils.logger import setup_logger
from validators.data_validator import DataValidator
from extractors.cv_extractor import CVExtractor  # Import correct
from fastapi import APIRouter, File, UploadFile, HTTPException
from processors.cv_processor import CVProcessor
from utils.logger import setup_logger

# Configuration du logger
logger = setup_logger()

# Création du router
router = APIRouter()

@router.post("/analyze")
async def analyze_cv(file: UploadFile = File(...)):
    """
    Endpoint pour analyser un CV
    """
    logger.info(f"Début de l'analyse du CV: {file.filename}")
    try:
        processor = CVProcessor()
        content = await file.read()
        result = await processor.process_cv(content, file.filename)

        logger.info(f"Analyse du CV réussie: {file.filename}")
        return {
            "status": "success",
            "data": result,
            "missing_information": processor.get_missing_information(result)
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse du CV {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




#
# @router.post("/analyze")
# async def analyze_cv(
#         file: UploadFile = File(...),
#         api_key: str = Depends(validate_api_key)
# ):
#     """
#     Endpoint pour analyser un CV
#     """
#     logger.info(f"Starting CV analysis for file: {file.filename}")
#
#     try:
#         processor = CVProcessor()
#         content = await file.read()
#         result = await processor.process_cv(content, file.filename)
#
#         logger.info(f"Successfully analyzed CV: {file.filename}")
#         return {
#             "status": "success",
#             "data": result,
#             "missing_information": processor.get_missing_information(result)
#         }
#     except Exception as e:
#         logger.error(f"Error analyzing CV {file.filename}: {str(e)}")
#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )