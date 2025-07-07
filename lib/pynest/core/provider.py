# lib.pynest/provider.py
import inspect
from typing import Any, get_origin

class Provider:
  def __init__(self) -> None:
    self._singletons: dict[type, Any] = {}
    self._bindings: dict[type, type] = {}
    
  def register(self, token: type, provider: type) -> None:
    self._bindings[token] = provider
  
  def provide(self, token: type):
    if token not in self._bindings:
      raise LookupError(f"No binding for {token}")

    impl = self._bindings[token]

    # If it's already a constructed instance, return it
    if not isinstance(impl, type):
      return impl

    # If already cached singleton, return it
    if impl in self._singletons:
      return self._singletons[impl]
    
    try:
      init_params = impl.__init__.__annotations__
    except AttributeError:
      init_params = {}
    
    deps = [self.provide(dep) for name, dep in init_params.items() if name != 'return']

    instance = impl(*deps)
    self._singletons[impl] = instance
    return instance

  def _construct(self, cls: type):
    if get_origin(cls) or cls.__module__ == 'builtins':
      raise TypeError(f"Cannot inject primitive/generic type {cls}")
    
    deps = []
    
    for p in inspect.signature(cls.__init__).parameters.values():
      if p.name == "self" or p.annotation is inspect._empty:
        continue
      
      deps.append(self.provide(p.annotation)) 
      
    return cls(*deps)

provider = Provider()