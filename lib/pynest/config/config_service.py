from typing import Any

class ConfigService:
  def __init__(self, data: dict[str, Any]):
    self._data = data

  def get(self, key: str, default: Any = None) -> Any:
    return self._data.get(key, default)

  def all(self) -> dict[str, Any]:
    return dict(self._data)