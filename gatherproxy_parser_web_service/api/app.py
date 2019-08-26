from aiohttp import web
from ..utils.app_initializer import AppInitializer
from ..common.constants import PROJECT_ROOT


app = web.Application()
config_file = PROJECT_ROOT / 'config' / 'config.yaml'
app_initializer = AppInitializer(config_file=config_file)
app_initializer.init_app(app)

app_settings = app_initializer.config["app_settings"]
host, port = app_settings["host"], app_settings["port"]

web.run_app(app, host=host, port=port)
