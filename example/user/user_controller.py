
from lib.pynest.core import controller, get, post, UseGuard
from .user_service import UserService

from example.roles_guard import Roles, RolesGuard, Public

# @UseGuard(RolesGuard)
@controller(prefix='/user', name="User")
class UserController:
  def __init__(self, user: UserService):
    self.user = user
    pass
  
  #@Public()
  @get('/')
  async def get_users(self):
    return await self.user.get_users()
  
  # @Roles("admin", "user")
  @get('/{user_id}')
  async def get_user(self, user_id: str):
    return await self.user.get_user(user_id)

  @post('/')
  def create_user(self, user_data: dict):
    return self.user.create_user(user_data)

  def update_user(self, user_id: int, user_data: dict):
    return self.user.update_user(user_id, user_data)

  def delete_user(self, user_id: int):
    return self.user.delete_user(user_id)