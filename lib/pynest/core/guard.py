# core/guard.py
import inspect
from fastapi import Request

def UseGuard(*guards):
  def wrap(obj):
    if isinstance(obj, type):
      obj.__pynest_class_guards__ = list(guards)
    else:
      existing = getattr(obj, '__pynest_method_guards__', [])
      obj.__pynest_method_guards__ = existing + list(guards)
    return obj
  
  return wrap


class CanActivate:
  def can_activate(self, request: Request) -> bool | None:
    raise NotImplementedError("Override can_activate()")

  async def _can_activate(self, request: Request) -> bool:
    method = self.can_activate
    if inspect.iscoroutinefunction(method):
      return await method(request)
    
    return method(request)