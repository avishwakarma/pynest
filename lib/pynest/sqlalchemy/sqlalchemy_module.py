from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from lib.pynest.core import make_async_module
from lib.pynest.core import module, injectable

from .model_proxy import ModelProxyMixin
from .token import DBSession, Base

class _SqlAlchemyInit: pass

class SqlAlchemyModule:
  @staticmethod
  def for_root_async(*, use_factory, inject=None):
    inject = inject or []

    async def factory_wrapper(*deps):
      cfg = use_factory(*deps)
      url = cfg.pop("url")
      auto_create = cfg.pop("auto_create", False)
      models = cfg.pop("models", {None})
      
      engine = create_async_engine(url, future=True)
      session_factory = async_sessionmaker(engine, expire_on_commit=False)
      
      for model in models.values():
        Base.metadata._add_table(model.__table__.name, model.__table__.schema, model.__table__)

      if auto_create:
        async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)

      @injectable()
      class SessionProvider(DBSession):
        def __call__(self):
          return session_factory()
        async def __aenter__(self):
          self._ctx = session_factory()
          return await self._ctx.__aenter__()
        async def __aexit__(self, *args):
          await self._ctx.__aexit__(*args)

      return {
        "providers": [ SessionProvider ],
        "bindings": { DBSession: SessionProvider }  # no need to bind again here
      }

    return make_async_module(
      token=_SqlAlchemyInit,
      base_cls=object,
      factory=factory_wrapper,
      inject=inject,
    )

  @staticmethod
  def for_feature(models):
    bindings = {}
    providers = []

    for model in models:
      proxy_cls = type(f"{model.__name__}Proxy", (model, ModelProxyMixin), {})
      
      ProviderCls = injectable()(
        type(
          f"{model.__name__}Provider",
          (proxy_cls,),
          {}
        )
      )

      providers.append(ProviderCls)
      bindings[model] = ProviderCls

    return module(
      providers=tuple(providers),
      exports=tuple(bindings),
      bindings=bindings
    )(type("SqlAlchemyFeatureModule", (), {}))