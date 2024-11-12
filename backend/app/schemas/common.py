from pydantic import BaseModel


class ListRequestDto(BaseModel):
    limit: int
    offset: int
