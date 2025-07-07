from cuid2 import Cuid
import uuid

_cuid_map = {}

def _device_fingerprint() -> str:
  mac = uuid.getnode()
  return f"{mac:012x}"

def cuid(length: int = 12) -> str:
  if not length in _cuid_map:
    _cuid_map[length] = Cuid(length=length, fingerprint=_device_fingerprint)

  return _cuid_map[length].generate()