import asyncio
from aiohttp import web
from ..utils.app_initializer import AppInitializer
from ..common.constants import PROJECT_ROOT

def main() -> None:
    # loop = asyncio.get_event_loop()
    app = web.Application()
    config_file = PROJECT_ROOT / 'config' / 'config.yaml'
    AppInitializer(config_file=config_file).init_app(app)

    """
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(conf))
    web.run_app(app, host=conf.app.host, port=conf.app.port)
    """
    web.run_app(app)
