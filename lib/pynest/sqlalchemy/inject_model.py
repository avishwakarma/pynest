from typing import Type

from .sqlalchemy_module import Base

def InjectModel(model_cls: Type[Base]): # type: ignore
  def wrapper(param):
    param.__pynest_inject_token__ = model_cls
    return param
  return wrapper

