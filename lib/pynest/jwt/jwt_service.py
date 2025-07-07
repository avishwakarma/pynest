# jwt/jwt_service.py

from jwt import encode, decode
from datetime import datetime, timedelta
from typing import Any, Dict
from lib.pynest.core.utils import to_seconds

class JwtService:
  def __init__(self, jwt_secret: str, expires_in: str, issuer: str, algorithm: str = 'HS256') -> None:
    self._jwt_secret = jwt_secret
    self._expires_in = expires_in
    self._issuer = issuer
    self._algorithm = algorithm
    
  def sign(self, payload: Dict[str, Any], expires_in: str = '') -> str:
    if not expires_in:
      expires_in = self._expires_in
      
    data = dict(payload)
    data["exp"] = datetime.utcnow() + timedelta(seconds=to_seconds(expires_in))
    data['iss'] = self._issuer

    return encode(data, self._jwt_secret, algorithm=self._algorithm)
  
  def verify(self, token: str) -> Dict[str, Any]:
    return decode(token, self._jwt_secret, algorithms=[self._algorithm], issuer=self._issuer)
