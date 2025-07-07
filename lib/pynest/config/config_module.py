from os import path
from typing import Callable, List, Optional
from dotenv import dotenv_values
from lib.pynest.core import module, injectable
from .config_service import ConfigService

class ConfigModule:
  @staticmethod
  def for_root(
    *, 
    load: Optional[List[Callable[[], dict]]] = [],
    envFilePath: Optional[str] = None
  ):
    config_data = {}
    
    if envFilePath:
      if not path.exists(envFilePath):
        raise FileNotFoundError(f"Environment file {envFilePath} does not exist.")
      config_data.update(dotenv_values(envFilePath))

    if len(load) > 0:
      for loader in load:
        config_data.update(loader())

    @injectable()
    class BoundConfigService(ConfigService):
      def __init__(self):
        super().__init__(config_data)

    return module(
      providers=[BoundConfigService],
      exports=[ConfigService],
      bindings={ConfigService: BoundConfigService}
    )(type("ConfigModule", (), {}))