from fastapi import APIRouter
from .calc_api import router as calc_router
api_router = APIRouter(prefix="/v1")
api_router.include_router(calc_router, prefix="/calc", tags=["calc"])