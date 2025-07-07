import inspect
import re
from functools import wraps
from typing import Optional, get_type_hints
from fastapi import FastAPI, Request, HTTPException
from fastapi.openapi.utils import get_openapi

from .provider import provider

_http_methods = ("get", "post", "put", "delete", "patch", "head", "options")

def collect(mod, seen, exported):
  if mod in seen:
    return
  
  seen.add(mod)

  for im in getattr(mod, "_imports", ()):
    collect(im, seen, exported)

  dup = set(mod._providers) & set().union(
    *(m._providers for m in seen if m is not mod)
  )
  
  if dup:
    raise RuntimeError(
      f"Provider {dup} declared twice; import its module instead"
    )
  
  exported[mod] = set(mod._exports)
  
def register_routes(instance):
  for attr in dir(instance):
    fn = getattr(instance, attr)
    if not (callable(fn) and hasattr(fn, "_route")):
      continue

    verb, path = fn._route
    if verb not in _http_methods and path in _http_methods:
      verb, path = path, verb

    class_guards = getattr(instance, "__pynest_class_guards__", [])
    method_guards = getattr(fn, "__pynest_method_guards__", [])
    guard_types = class_guards + method_guards

    sig = inspect.signature(fn)
    req_param_name = next((
      p.name
      for p in sig.parameters.values()
      if p.name != "self"
      and (
        p.name == "request"
        or p.annotation is Request
        or p.default is Request
      )), None
    )
    
    wants_req = req_param_name is not None
    is_async = inspect.iscoroutinefunction(fn)

    def make_handler(_fn, _guards, _wants_req, req_param_name, _is_async):
      @wraps(_fn, assigned=("__module__", "__name__", "__qualname__", "__doc__"))
      async def handler(request: Request, **kwargs):
        request.get_handler = lambda: _fn

        # run guards
        for guard_cls in _guards:
          guard = provider.provide(guard_cls)
          
          if not await guard._can_activate(request):
            raise HTTPException(status_code=403, detail="Forbidden")

        if _wants_req:
          kwargs[req_param_name] = request
        else:
          kwargs.pop("request", None)

        return await _fn(**kwargs) if _is_async else _fn(**kwargs)
      
      orig_sig = inspect.signature(_fn)
      new_params = [inspect.Parameter(
        "request",  
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Request
      )]
      
      for name, param in orig_sig.parameters.items():
        if name != "self":
          new_params.append(param.replace(kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
      
      handler.__signature__ = inspect.Signature(new_params)

      return handler

    handler = make_handler(fn, guard_types, wants_req, req_param_name, is_async)
    instance.router.add_api_route(path, handler, methods=[verb.upper()])
    
    
def instantiate_with_di(cls):
  sig = inspect.signature(cls.__init__)
  hints = get_type_hints(cls.__init__)
  deps = [
    provider.provide(hints[p.name])
    for p in sig.parameters.values()
    if p.name != "self" and p.annotation is not inspect._empty
  ]
  
  return cls(*deps)

def default_openapi_schema(app: FastAPI, options: Optional[dict] = {}):
  if app.openapi_schema:
    return app.openapi_schema
  
  schema = get_openapi(
    title=options.get("title", "Pynest API"),
    version=options.get("version", "1.0.0"),
    description=options.get("description", "API documentation for Pynest application"),
    routes=app.routes,
  )
  
  if options.get('swagger_auth', False):
    schema.setdefault("components", {})
    schema["components"].setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"] = {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    }
  
  for path in schema["paths"].values():
    for method in path.values():
      method.setdefault("security", []).append({"BearerAuth": []})
  
  return schema

def to_seconds(duration: str) -> int:
  time_units = {
    'y': 365 * 86400,
    'mon': 30 * 86400,
    'w': 7 * 86400,
    'd': 86400,
    'h': 3600,
    'm': 60,
    's': 1
  }

  # Match in order: mon (to avoid confusion with 'm'), then y/w/d/h/m/s
  pattern = re.compile(r'(\d+)(mon|y|w|d|h|m|s)')
  matches = pattern.findall(duration.lower())

  total_seconds = 0
  for value, unit in matches:
    total_seconds += int(value) * time_units[unit]
  
  return total_seconds