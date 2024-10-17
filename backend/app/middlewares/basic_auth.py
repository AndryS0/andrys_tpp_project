from base64 import b64decode

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class DocsAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, username: str, password: str):
        super().__init__(app)
        self.username = username
        self.password = password

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
            auth = request.headers.get("Authorization")
            if not auth:
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

            scheme, _, credentials = auth.partition(" ")
            if scheme.lower() != "basic":
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

            try:
                decoded = b64decode(credentials).decode("utf-8")
                username, password = decoded.split(":", 1)
            except ValueError:
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

            if username != self.username or password != self.password:
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

        response = await call_next(request)
        return response
