from os import path
from lib.pynest.core import module
from lib.pynest.config import ConfigModule, ConfigService
from lib.pynest.jwt import JwtModule
from lib.pynest.sqlalchemy import SqlAlchemyModule
from lib.models.dict import models

from .user.user_module import UserModule

def jwt_factory(config: ConfigService):  
  return {
    "jwt_secret": config.get('JWT_SECRET_KEY') or 'fT6vJzElMX0LzAmv9q7kKptuHYOe9PxTQ3dQgG6KvPs',
    "expires_in": config.get('JWT_EXPIRY') or '1d',
    "issuer": config.get('JWT_ISSUER') or 'lib.pynest',
    "algorithm": config.get('JWT_ALGORITHM') or 'HS256'
  }
  
def database_factory(config: ConfigService):
  url = f"postgresql+asyncpg://{config.get('DB_USER', 'postgres')}:" \
    f"{config.get('DB_PASSWORD', '')}@" \
    f"{config.get('DB_HOST', 'localhost')}:" \
    f"{config.get('DB_PORT', '5432')}/" \
    f"{config.get('DB_NAME', 'lib.pynest')}"
  
  return {
    "url": url,
    "auto_create": True,
    "models": models
  }

@module(
  imports=[
    SqlAlchemyModule.for_root_async(
      inject=[ConfigService],
      use_factory=database_factory
    ),
    ConfigModule.for_root(
      envFilePath=path.join(path.dirname(__file__), "../.env"),
    ),
    JwtModule.for_root_async(
      inject=[ConfigService],
      use_factory=jwt_factory,
    ),
    UserModule
  ],
)
class AppModule:
  pass