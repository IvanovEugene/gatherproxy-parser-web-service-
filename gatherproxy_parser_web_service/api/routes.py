from aiohttp import web
from .views import CollectRequestHandler


class RoutesInstaller:
    def __init__(self, app: web.Application, handler: CollectRequestHandler):
        self._routes = [
            web.get("/v1/health", handler.health, name="health"),
            web.get('/v1/proxy-collector', handler.swagger, name="proxy-collector-swagger"),
            web.post('/v1/proxy-collector/collect', handler.collect, name="proxy-collector-collect")
        ]
        self._app = app
        self._handler = handler

    def install(self):
        self._app.add_routes(self._routes)
