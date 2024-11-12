from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.dependencies.id_token_validator import check_api_token
from app.schemas.common import ListRequestDto
from app.schemas.planet_schema import UpdatePlanetRequest, CreatePlanetRequest, DeletePlanetRequest, PlanetSchema
from app.services.planet_service import PlanetService

router = APIRouter(
    dependencies=[Depends(check_api_token)]
)


@router.get("")
async def list_planets(
    request: Annotated[ListRequestDto, Query()],
    planet_service: PlanetService = Depends(PlanetService)
) -> List[PlanetSchema]:
    return await planet_service.get_planets(request.limit, request.offset)


@router.patch("")
async def update_planet(
        request: Annotated[UpdatePlanetRequest, Query()],
        planet_service: PlanetService = Depends(PlanetService)
) -> PlanetSchema:
    return await planet_service.update_planet(request)


@router.post("")
async def create_planet(
        request: Annotated[CreatePlanetRequest, Query()],
        planet_service: PlanetService = Depends(PlanetService)
) -> PlanetSchema:
    return await planet_service.add_new_planet(request)


@router.delete("")
async def delete_planet(
        request: Annotated[DeletePlanetRequest, Query()],
        planet_service: PlanetService = Depends(PlanetService)
):
    return await planet_service.delete_planet(request.id)

