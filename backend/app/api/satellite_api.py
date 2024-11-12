from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.dependencies.id_token_validator import check_api_token
from app.schemas.common import ListRequestDto
from app.schemas.satellite_schema import UpdateSatelliteRequest, CreateSatelliteRequest, DeleteSatelliteRequest, \
    SatelliteSchema
from app.services.satellite_service import SatelliteService

router = APIRouter(
    dependencies=[Depends(check_api_token)]
)


@router.get("")
async def list_satellites(
    request: Annotated[ListRequestDto, Query()],
    satellite_service: SatelliteService = Depends(SatelliteService)
) -> List[SatelliteSchema]:
    return await satellite_service.get_satellites(request.limit, request.offset)


@router.patch("")
async def update_satellite(
        request: Annotated[UpdateSatelliteRequest, Query()],
        satellite_service: SatelliteService = Depends(SatelliteService)
) -> SatelliteSchema:
    return await satellite_service.update_satellite(request)


@router.post("")
async def create_satellite(
        request: Annotated[CreateSatelliteRequest, Query()],
        satellite_service: SatelliteService = Depends(SatelliteService)
) -> SatelliteSchema:
    return await satellite_service.add_new_satellite(request)


@router.delete("")
async def delete_satellite(
        request: Annotated[DeleteSatelliteRequest, Query()],
        satellite_service: SatelliteService = Depends(SatelliteService)
):
    return await satellite_service.delete_satellite(request.id)
