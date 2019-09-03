from aiohttp import web
from .views import CollectV1Handler
from aiohttp_apispec import setup_aiohttp_apispec


class RoutesInstaller:
    def __init__(self, app: web.Application, handler: CollectV1Handler):
        self._routes = [
            web.get("/health", handler.health, name="health"),
            web.post('/api/v1/proxy-collector/collect', handler.collect,
                     name="proxy-collector-collect")
        ]
        self._app = app
        self._handler = handler

    def install(self):
        self._app.add_routes(self._routes)

        setup_aiohttp_apispec(
            app=self._app,
            title="Documentation of gatherproxy_parser_web_service",
            version="v1",
            url="/api/docs/swagger.json",
            swagger_path="/api/docs",
        )
