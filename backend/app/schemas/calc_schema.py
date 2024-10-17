from pydantic import BaseModel


class CalcRequest(BaseModel):
    expression: str


class CalcResponse(BaseModel):
    answer: float
