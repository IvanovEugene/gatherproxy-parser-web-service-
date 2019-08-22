import asyncio
from aiohttp import web
from .routes import setup_routes
from .views import CollectRequestHandler


def main() -> None:
    loop = asyncio.get_event_loop()
    app = web.Application()
    collect_handler = CollectRequestHandler()
    setup_routes(app=app, handler=collect_handler)
    """
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(conf))
    web.run_app(app, host=conf.app.host, port=conf.app.port)
    """
    web.run_app(app)