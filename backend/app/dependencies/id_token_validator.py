from typing import Annotated

from fastapi import Security, HTTPException

from app.core.security import verify_token, x_api_token_header


async def check_api_token(x_api_token: Annotated[str | None, Security(x_api_token_header)] = None):
    if not verify_token(x_api_token):
        raise HTTPException(status_code=403, detail={"message": "Invalid API Token"})
