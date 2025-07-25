from fastapi import APIRouter

from app.api.endpoints import completion, document, reference, academic, style

api_router = APIRouter()
api_router.include_router(completion.router, prefix="/completion", tags=["completion"])
api_router.include_router(document.router, prefix="/document", tags=["document"])
api_router.include_router(reference.router, prefix="/reference", tags=["reference"])
api_router.include_router(academic.router, prefix="/academic", tags=["academic"])
api_router.include_router(style.router, prefix="/style", tags=["style"])
