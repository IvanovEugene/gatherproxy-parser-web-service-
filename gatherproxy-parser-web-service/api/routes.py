from aiohttp import web
from .views import CollectRequestHandler


def setup_routes(app: web.Application, handler: CollectRequestHandler):
    ROUTES = [
        web.get("/v1/health", handler.health, name="health"),
        web.get('/v1/proxy-collector', handler.swagger, name="proxy-collector-swagger"),
        web.post('/v1/proxy-collector/collect', handler.collect, name="proxy-collector-collect")
    ]

    app.add_routes(ROUTES)
