import logging
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from .api import api_router
from .core import settings
from .middlewares import DocsAuthMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await startup()
    yield
    await shutdown()


logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        logger.info(f"Request: {request.method} {request.url}")

        # Measure the time taken to process the request
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        # Log the outgoing response
        logger.info(
            f"Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f} secs"
        )

        return response


app = FastAPI(lifespan=lifespan)
# ignore this warning, pycharm problem
# BaseHTTPMiddleware implicitly implements _MiddlewareClass of starlette
# noinspection PyTypeChecker
app.add_middleware(DocsAuthMiddleware, username=settings.swagger_user, password=settings.swagger_password)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(repr(exc))},
    )


# This will be used in future after adding DB connections
async def startup():
    pass


async def shutdown():
    pass


def start():
    uvicorn.run(app, host=settings.host, port=settings.port)
