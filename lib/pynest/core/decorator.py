# lib.pynest/decorator.py
from fastapi import APIRouter

def injectable():
  def wrap(cls):
    cls._injectable = True
    return cls
  return wrap

def module(*, providers=(), controllers=(), imports=(), bindings={}, exports=()):
  def wrap(cls):
    valid_exports = set(providers) | bindings.keys()
    invalid_exports = [exp for exp in exports if exp not in valid_exports]
    
    if invalid_exports:
      raise ValueError(f"Only providers can be exported. Invalid: {invalid_exports}")
    
    ctrl_set = set(controllers)
    
    for p in providers:
      if not getattr(p, '_injectable', False):
        print(f"⚠️  Warning: {p.__name__} is listed as a provider but not decorated with @injectable")
    
    if any(exp in ctrl_set for exp in exports):
      raise ValueError("Controllers cannot be exported.")

    cls._providers   = tuple(dict.fromkeys(providers))
    cls._controllers = controllers
    cls._imports     = imports
    cls._bindings    = bindings
    cls._exports     = exports

    return cls
  return wrap

def controller(prefix='', name: str = None):
  def wrap(cls):
    cls.router = APIRouter(prefix=prefix, tags=[name] if name else [cls.__name__])
    return cls
  return wrap


def _route(method: str, path: str):
  def wrap(func):
    func._route = {method, path}
    return func
  return wrap

def get(path: str):
  return _route("get", path)
  
def post(path: str):
  return _route("post", path)

def put(path: str):
  return _route("put", path)

def delete(path: str):
  return _route("delete", path)

def patch(path: str):
  return _route("patch", path)

def head(path: str):
  return _route("head", path)

def options(path: str):
  return _route("options", path)  
