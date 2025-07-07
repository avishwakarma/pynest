from lib.models.user import User
from lib.pynest.core import module
from lib.pynest.sqlalchemy import SqlAlchemyModule

from .user_controller import UserController
from .user_service import UserService

@module(
  imports=[SqlAlchemyModule.for_feature([User])],
  providers=[UserService],
  controllers=[UserController],
)
class UserModule:
  pass