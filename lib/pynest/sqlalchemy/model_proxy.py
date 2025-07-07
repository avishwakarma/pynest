from typing import Any, List, Optional, TypeVar
from sqlalchemy import select, update as sa_update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from lib.pynest.core.provider import provider

from .token import DBSession     # DI token resolved to AsyncSession

T = TypeVar("T", bound="ModelProxyMixin")

class ModelProxyMixin:
    @classmethod
    def _session(cls) -> AsyncSession:
        session_provider = provider.provide(DBSession)
        if callable(session_provider):
          return session_provider()
        raise RuntimeError("Could not obtain a session.")
      
    @classmethod
    async def db(cls) -> AsyncSession:
      return cls._session()

    @classmethod
    async def all(cls: T) -> List[T]:
      db = cls._session()
      result = await db.execute(select(cls))
      return result.scalars().all()

    @classmethod
    async def first(cls: T) -> Optional[T]:
      db = cls._session()
      result = await db.execute(select(cls).limit(1))
      return result.scalars().first()

    @classmethod
    async def get(cls: T, pk: Any) -> Optional[T]:
      db = cls._session()
      return await db.get(cls, pk)

    @classmethod
    async def filter_by(cls: T, **filters) -> List[T]:
      db = cls._session()
      result = await db.execute(select(cls).filter_by(**filters))
      return result.scalars().all()

    @classmethod
    async def count(cls) -> int:
      db = cls._session()
      result = await db.execute(select(cls))
      return result.scalars().count()

    @classmethod
    async def create(cls: T, **data) -> T:
      """
      Insert a new row and commit the transaction.
      Returns the created instance (with PK populated).
      """
      db = cls._session()
      obj = cls(**data)
      db.add(obj)
      await db.commit()
      await db.refresh(obj)
      return obj

    @classmethod
    async def update(cls: T, pk: Any, **data) -> Optional[T]:
      """
      Update row by primary key. Returns updated instance (or None).
      """
      db = cls._session()
      await db.execute(sa_update(cls).where(cls.__table__.primary_key.columns.values()[0] == pk).values(**data))
      await db.commit()
      return await cls.get(pk)

    @classmethod
    async def delete(cls: T, pk: Any) -> bool:
      """
      Delete row by primary key. Returns True if something was deleted.
      """
      db = cls._session()
      result = await db.execute(sa_delete(cls).where(cls.__table__.primary_key.columns.values()[0] == pk))
      await db.commit()
      return result.rowcount > 0