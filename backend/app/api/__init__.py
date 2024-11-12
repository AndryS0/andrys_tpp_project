from fastapi import APIRouter
from .calc_api import router as calc_router
from .planet_api import router as planet_router
from .star_api import router as star_router
from .satellite_api import router as satellite_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(calc_router, prefix="/calc", tags=["calc"])
api_router.include_router(planet_router, prefix="/planet", tags=["planet"])
api_router.include_router(star_router, prefix="/star", tags=["star"])
api_router.include_router(satellite_router, prefix="/satellite", tags=["satellite"])
