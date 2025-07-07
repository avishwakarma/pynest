from lib.pynest.core import CanActivate, SetMetadata, relector
from lib.pynest.jwt import JwtService

Roles = lambda *roles: SetMetadata("roles", roles)
Public = lambda: SetMetadata("roles", ["public"])

class RolesGuard(CanActivate):
  def __init__(self, jwt: JwtService):
    super().__init__()
    self.jwt = jwt
    
  def can_activate(self, request):
    roles = relector.get("roles", request.get_handler())
    
    if("public" in roles):
      return True

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not token:
      return False
    
    verified = None
    
    try:
      verified = self.jwt.verify(token)
    except Exception as e:
      return False
    
    request.state.user = verified.get("user", {})
    
    return True