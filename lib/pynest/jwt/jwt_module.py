# jwt/jwt_module.py

from lib.pynest.core import make_async_module
from .jwt_service import JwtService

class JwtModule:
  @staticmethod
  def for_root(
    *,
    jwt_secret: str,
    expires_in: str,
    issuer: str,
    algorithm: str = "HS256"
  ):
    def _factory():
      return dict(
        jwt_secret=jwt_secret, 
        expires_in=expires_in, 
        issuer=issuer, 
        algorithm=algorithm
      )

    return JwtModule.for_root_async(use_factory=_factory)
  
  @staticmethod
  def for_root_async(
    *,
    use_factory: callable = None,
    inject: list[type] = [],
  ):
    return make_async_module(
      token=JwtService,
      base_cls=JwtService,
      factory=use_factory,
      inject=inject
    )
