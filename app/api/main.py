from fastapi import APIRouter

from app.api.routes import ocr

api_router = APIRouter()

api_router.include_router(ocr.router)