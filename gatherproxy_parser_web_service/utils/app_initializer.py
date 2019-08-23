import yaml
from os import path
from aiohttp import web
from ..common.exceptions import (ConfigFileNotExists, ConfigFileParsingException, ConfigValidationException)
from ..utils.logging import Logging
from .schemas import ConfigSchema
from ..api.routes import RoutesInstaller
from ..api.views import CollectRequestHandler


class AppInitializer:
    def __init__(self, config_file: str):
        self._logger = Logging.get_logger(name=__name__)
        self._config_file = config_file
        self._config = None

    def _get_config_from_file(self) -> dict:
        if not path.exists(self._config_file):
            self._logger.error(f'File "{self._config_file}" not exists')
            raise ConfigFileNotExists(f'File "{self._config_file}" not exists')

        try:
            with open(file=self._config_file, mode="r") as file:
                config = yaml.load(file)
        except Exception as config_parse_exception:
            self._logger.error(f'Can not parse file "{self._config_file}": {str(config_parse_exception)}')
            raise ConfigFileParsingException(f'Can not parse file "{self._config_file}"')

        return config

    @property
    def config(self) -> dict:
        if not self._config:
            config_content = self._get_config_from_file()
            self._logger.debug(f'Config file {self._config_file} parsed successfully')
            try:
                self._config = ConfigSchema().load(config_content)
                self._logger.debug(f'Config has correct format: {config_content}')
            except Exception as validation_exception:
                self._logger.error(f'YAML config has incorrect format (has excess or missed keys):'
                                   f' {str(validation_exception)}')
                raise ConfigValidationException('YAML config has incorrect format (has excess or missed keys)')

        return self._config

    def init_app(self, app: web.Application) -> None:
        RoutesInstaller(app=app, handler=CollectRequestHandler()).install()
        print(self.config)
