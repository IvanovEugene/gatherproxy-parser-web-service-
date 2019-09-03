from gatherparser import ProxyParser
from gatherparser.engine.drivers import ChromeDriver


class SyncProxyParserWorker:
    """
    class-wrapper for ProxyParser because ProcessPoolExecutor
    does not works with classes which contain async functions
    """
    def __init__(self, driver_params: dict):
        self._driver_params = driver_params

    def _get_chrome_driver(self) -> ChromeDriver:
        chrome_driver_kwargs = {
            "driver_path": self._driver_params["driver_path"],
            "page_load_timeout": self._driver_params["timeout"]
        }

        return ChromeDriver(**chrome_driver_kwargs).get_driver()

    def _get_proxy_parser(self, driver: ChromeDriver) -> ProxyParser:
        return ProxyParser(driver=driver)

    def parse(self, page_count: int, url_to_parse: str) -> set:
        proxy_parser = self._get_proxy_parser(driver=self._get_chrome_driver())
        return proxy_parser.get_proxies_by_page_count(page_count=page_count,
                                                      url_to_parse=url_to_parse)
