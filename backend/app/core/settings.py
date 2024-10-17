from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    x_api_token: Optional[str] = '12345'
    port: Optional[int] = 8000
    host: Optional[str] = '127.0.0.1'
    swagger_user: Optional[str] = 'swagger'
    swagger_password: Optional[str] = 'swagger'

    model_config = SettingsConfigDict(env_file=".env")


