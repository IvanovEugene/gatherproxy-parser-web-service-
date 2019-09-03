from asyncio import get_event_loop
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from gatherparser import ProxyValidator
from .sync_proxy_parser_worker import SyncProxyParserWorker
from ..common.logging import Logging


class AsyncProxyCollector:
    def __init__(self, driver_params: dict, validator_params: dict,
                 parser_max_workers: int):
        self._executor = ProcessPoolExecutor(max_workers=parser_max_workers)
        self._driver_params = driver_params
        self._validator_params = validator_params
        self._proxy_validator = self._get_proxy_validator()
        self._logger = Logging.get_logger(name=__name__)

    def _get_proxy_validator(self) -> ProxyValidator:
        validator_kwargs = {
            "proxy_verification_link": self._validator_params[
                "verification_link"],
            "proxy_timeout": self._validator_params["timeout"]
        }
        return ProxyValidator(**validator_kwargs)

    async def _validate(self, proxies: set) -> set:
        valid_proxies = await self._proxy_validator.get_available_proxies(
            proxies_to_check=proxies)
        return valid_proxies

    async def collect(self, page_count: int, url_to_parse: str, request_id: int,
                      validate: bool = True) -> set:
        # run parser worker in ProcessPoolExecutor
        event_loop = get_event_loop()
        self._logger.debug("Start to collecting proxies",
                           extra={"page_count": page_count,
                                  "url_to_parse": url_to_parse,
                                  "request_id": request_id
                                  }
                           )
        proxy_parser_worker = SyncProxyParserWorker(
            driver_params=self._driver_params)
        self._logger.debug("SyncProxyParserWorker created",
                           extra={"request_id": request_id})
        asnyc_parse = partial(proxy_parser_worker.parse, page_count=page_count,
                              url_to_parse=url_to_parse)
        proxies = await event_loop.run_in_executor(executor=self._executor,
                                                   func=asnyc_parse)
        self._logger.info("Proxies collected", extra={"request_id": request_id})
        if not validate:
            return proxies
        self._logger.debug("Start to validating collected proxies",
                           extra={"request_id": request_id})
        # run validation in event loop
        valid_proxies = await self._validate(proxies)
        self._logger.info("Proxies validated", extra={"request_id": request_id})
        return valid_proxies
