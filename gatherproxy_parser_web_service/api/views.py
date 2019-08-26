from aiohttp import web
from asyncio import Lock
from aiohttp_apispec import request_schema, docs
from .schemas import CollectRequestSchema
from ..async_proxy_collector.async_proxy_collector import AsyncProxyCollector
from ..common.logging import Logging


class CollectV1Handler:
    def __init__(self, app_config: dict):
        self._async_proxy_collector = AsyncProxyCollector(
            driver_params=app_config["driver_params"], validator_params=app_config["validator_params"],
            parser_max_workers=app_config["app_settings"]["parser_max_workers"])
        self._logger = Logging.get_logger(name=__name__)
        self._collect_request_id = 0

    @docs(
        summary="Health check endpoint",
    )
    async def health(self, request: web.Request) -> web.Response:
        return web.Response(body="OK")

    async def swagger(self, request: web.Request) -> web.Response:
        return web.Response(body="OK")

    @docs(
        summary="Endpoint for collecting and returning in response list of proxies by given parameters"
    )
    @request_schema(CollectRequestSchema())
    async def collect(self, request: web.Request) -> web.Response:
        incr_lock = Lock()  # Mutex for self._collect_request_id increment
        async with incr_lock:
            request_id = self._collect_request_id
            self._collect_request_id += 1
        post_data = await request.text()
        self._logger.info(f"New request {self._collect_request_id}", extra={"request_id": request_id})
        try:
            form = CollectRequestSchema().loads(post_data)
        except Exception as validation_exception:
            self._logger.warning(f"Incorrect request body. {validation_exception}", extra={"request_id": request_id})
            return web.json_response(data={"status": "Incorrect request body", "data": {},
                                           "errors": [str(validation_exception)]}, status=400)

        try:
            self._logger.info(f"Request body correct", extra={"request_id": request_id})
            proxies = await self._async_proxy_collector.collect(page_count=form["page_count"], url_to_parse=form["url"],
                                                                validate=form["validate"], request_id=request_id)
            proxies = tuple(proxies)
            self._logger.info(f"Request handled", extra={"request_id": request_id})
            return web.json_response(data={"status": "ok", "data": {"proxies": proxies},
                                           "errors": []}, status=200)
        except Exception as parse_exception:
            self._logger.error(f"Internal server error: {parse_exception}.", extra={"request_id": request_id})
            return web.json_response(data={"status": "Internal server error", "data": {},
                                           "errors": [str(parse_exception)]}, status=500)
