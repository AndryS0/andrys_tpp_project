from typing import Annotated

import numexpr
from fastapi import APIRouter, Depends, Query, HTTPException

from app.dependencies.id_token_validator import check_api_token
from app.schemas import CalcRequest, CalcResponse

router = APIRouter(
    dependencies=[Depends(check_api_token)]
)


@router.get("")
async def calc(
        request: Annotated[CalcRequest, Query()]
) -> CalcResponse:
    try:
        response = CalcResponse(answer=numexpr.evaluate(request.expression).item())
        return response
    except KeyError:
        raise HTTPException(status_code=400, detail="Wrong key")
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Syntax error")
    except Exception:
        raise HTTPException(status_code=400, detail="Something unknown went wrong")
