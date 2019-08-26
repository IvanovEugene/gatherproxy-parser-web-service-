from aiohttp import web
from .views import CollectV1Handler


class RoutesInstaller:
    def __init__(self, app: web.Application, handler: CollectV1Handler):
        self._routes = [
            web.get("/health", handler.health, name="health"),
            web.get('/api/v1/proxy-collector', handler.swagger, name="proxy-collector-swagger"),
            web.post('/api/v1/proxy-collector/collect', handler.collect, name="proxy-collector-collect")
        ]
        self._app = app
        self._handler = handler

    def install(self):
        self._app.add_routes(self._routes)
