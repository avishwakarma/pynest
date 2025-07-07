# core/metadata.py
def SetMetadata(key: str, value):
  def decorator(func):
    if not hasattr(func, '__pynest_meta__'):
      func.__pynest_meta__ = {}
    
    func.__pynest_meta__[key] = value
    
    return func
  
  return decorator

class Reflector:
  def get(self, key: str, handler):
    return getattr(handler, "__pynest_meta__", {}).get(key)
  
relector = Reflector()