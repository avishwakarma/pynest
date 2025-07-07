# lib.pynest/core/bootstrap.py
from typing import Optional
from fastapi import FastAPI

from .provider  import provider
from .utils import register_routes, instantiate_with_di, collect, default_openapi_schema

def bootstrap(root_module, options: Optional[dict] = None) -> FastAPI:
  seen, exported = set(), {}
  collect(root_module, seen, exported)

  for mod in seen:
    for prov in mod._providers:
      provider.register(prov, prov)

    for token, impl in mod._bindings.items():
      provider.register(token, impl)

  app = FastAPI()

  for mod in seen:
    hook = getattr(mod, '__pynest_startup__', None)
    if hook:
      hook(app)
      
    for ctrl in mod._controllers:
      instance = instantiate_with_di(ctrl)
      register_routes(instance)
      app.include_router(instance.router)
      
  if options:
    app.title = options.get('title', 'Pynest Application')
    app.description = options.get('description', '')
    app.version = options.get('version', '0.1.0')
    app.license_info = options.get('license_info', None)
    app.openapi_tags = options.get('tags', [])
    
    if options.get('openapi_schema'):
      app.openapi_schema = options['openapi_schema']
    else:
      app.openapi_schema = default_openapi_schema(app, options=options)

  return app