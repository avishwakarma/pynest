from lib.models.user import User
from lib.pynest.core import injectable
from lib.pynest.config import ConfigService
@injectable()
class UserService:
  def __init__(self, config: ConfigService, user: User):
    self.config = config
    self.user = user
    
  async def get_users(self):
    return await self.user.all()

  async def get_user(self, user_id: str):
    return await self.user.get(user_id)
  
  def echo(self):
    return 'echo: user service'

  def create_user(self, user_data: dict):
    return f'create_user: {user_data}'

  def update_user(self, user_id: int, user_data: dict):
    return 'update_user'

  def delete_user(self, user_id: int):
    return 'delete_user'