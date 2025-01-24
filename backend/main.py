from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.security import validate_api_key
from api.endpoints import documents
from utils.logger import setup_logger
from api.endpoints import documents, cv

app = FastAPI(
    title="Document Processing API",
    description="API pour le traitement intelligent de documents",
    version="1.0.0"
)

# Configuration du logger
logger = setup_logger()

settings = get_settings()

# Middleware pour logger toutes les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code}")
    return response

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    logger.info("Root endpoint called")
    return {
        "status": "online",
        "message": "Welcome to Document Processing API",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check(api_key: str = Depends(validate_api_key)):
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "environment": "development"
    }

app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"]
)

app.include_router(
    cv.router,
    prefix="/api/v1/cv",
    tags=["CV"]
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return {
        "status": "error",
        "message": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
















#
#
#
#
#
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
# @app.get("/test")
# def read_test():
#     return {"message": "This is a test endpoint"}