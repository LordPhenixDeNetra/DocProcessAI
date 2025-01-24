# utils/logger.py
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger():
    # Créer le dossier logs s'il n'existe pas
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    # Configuration du logger
    logger = logging.getLogger("doc_processing_api")
    logger.setLevel(logging.DEBUG)

    # Configuration du format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler pour le fichier
    file_handler = logging.FileHandler(
        f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger











# # backend/utils/logger.py
# import logging
# import sys
# from pathlib import Path
# from loguru import logger
# import json
# from datetime import datetime
#
# # Configuration des logs
# def setup_logger():
#     # Créer le dossier logs s'il n'existe pas
#     log_path = Path("logs")
#     log_path.mkdir(exist_ok=True)
#
#     # Format personnalisé pour les logs
#     log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
#
#     # Configuration de loguru
#     config = {
#         "handlers": [
#             {
#                 "sink": sys.stdout,
#                 "format": log_format,
#                 "colorize": True,
#                 "level": "DEBUG"
#             },
#             {
#                 "sink": f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
#                 "format": log_format,
#                 "rotation": "00:00",  # Nouveau fichier chaque jour
#                 "retention": "30 days",
#                 "compression": "zip",
#                 "level": "INFO"
#             }
#         ]
#     }
#
#     # Appliquer la configuration
#     logger.configure(**config)
#     return logger
#
# # Fonction pour logger les requêtes
# async def log_request(request, response_body):
#     log_dict = {
#         "timestamp": datetime.now().isoformat(),
#         "client_ip": request.client.host,
#         "method": request.method,
#         "url": str(request.url),
#         "headers": dict(request.headers),
#         "response_status": response_body.get("status", "N/A"),
#         "response_body": response_body
#     }
#     logger.info(f"Request processed: {json.dumps(log_dict, indent=2)}")