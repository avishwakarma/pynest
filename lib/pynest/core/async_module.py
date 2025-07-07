import inspect
from fastapi import FastAPI
from .decorator import module, injectable
from .provider import provider 

def make_async_module(*, token, base_cls, factory, inject):
  _settings = {}

  async def _run_factory():
    deps = [provider.provide(dep) for dep in inject]
    result = factory(*deps)
    
    if inspect.iscoroutine(result):
      result = await result
    
    for tkn, impl in result.get("bindings", {}).items():
      provider._bindings[tkn] = impl 
    
    _settings.update(result)

  @injectable()
  class BoundProvider(base_cls):
    def __init__(self):
      if not _settings:
        raise RuntimeError(f"{base_cls.__name__} accessed before factory run")
      if hasattr(super(), '__init__'):
        try:
          super().__init__(**_settings)
        except TypeError:
          super().__init__()

  Generated = type(f"Async{token.__name__}Module", (), {})

  def register_startup(app: FastAPI):
    @app.on_event("startup")
    async def _():
      await _run_factory()

  Generated.__pynest_startup__ = register_startup

  return module(
    providers=[BoundProvider],
    exports=[token],
    bindings={
      token: BoundProvider,
    }
  )(Generated)