from typing import Annotated, Union

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core import settings

x_api_token_header = APIKeyHeader(name='x-api-token')


def verify_token(token: str) -> bool:
    return token == settings.x_api_token


