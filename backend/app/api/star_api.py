from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.dependencies.id_token_validator import check_api_token
from app.schemas.common import ListRequestDto
from app.schemas.star_schema import UpdateStarRequest, CreateStarRequest, DeleteStarRequest, StarSchema
from app.services.star_service import StarService

router = APIRouter(
    dependencies=[Depends(check_api_token)]
)


@router.get("")
async def list_stars(
    request: Annotated[ListRequestDto, Query()],
    star_service: StarService = Depends(StarService)
) -> List[StarSchema]:
    return await star_service.get_stars(request.limit, request.offset)


@router.patch("")
async def update_star(
        request: Annotated[UpdateStarRequest, Query()],
        star_service: StarService = Depends(StarService)
) -> StarSchema:
    return await star_service.update_star(request)


@router.post("")
async def create_star(
        request: Annotated[CreateStarRequest, Query()],
        star_service: StarService = Depends(StarService)
) -> StarSchema:
    return await star_service.add_new_star(request)


@router.delete("")
async def delete_star(
        request: Annotated[DeleteStarRequest, Query()],
        star_service: StarService = Depends(StarService)
):
    return await star_service.delete_star(request.id)
