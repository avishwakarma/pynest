from sqlalchemy import Column, String, TIMESTAMP

from lib.pynest.sqlalchemy import Base

from lib.utils import cuid

class BaseModel(Base):
  __abstract__ = True
  id = Column(String(12), primary_key=True, default=cuid)
  created_at = Column(TIMESTAMP, nullable=False, server_default="NOW()")
  updated_at = Column(TIMESTAMP, nullable=False, server_default="NOW()", onupdate="NOW()")