from lib.pynest.core import bootstrap
from example.app_module import AppModule

app = bootstrap(AppModule, options={
  "name": "Pynest Application",
  "description": "A simple Pynest application",
  "version": "0.1.0",
  "swagger_auth": True
})