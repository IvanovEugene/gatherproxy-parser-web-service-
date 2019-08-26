# gatherproxy-parser-web-service
Asynchronous web-wrapper for [gatherproxy-parser](https://github.com/IvanovEugene/gatherproxy-parser)

## Service components
- `SyncProxyParserWorker` - synchronous wrapper-class for `ProxyParser`. Runs in `ProcessPoolExecutor` because `ProxyParser` uses I/O blocking code (`Selenium`)
- `AsyncProxyCollector` - Asynchronous wrapper-class of `ProxyValidator` and `SyncProxyParserWorker` that encapsulates collecting and validating

## API endpoints
```
GET /health
Description: health check endpoint
Response:
  body:
    "OK"

GET /api/docs/swagger.json
Description: Specification

GET /api/docs
Description: Swagger UI

POST /v1/proxy-collector/collect
Request:
  headers:
    Content-Type: application/json
  body:
    JSON-object with keys:
      url-to-parse (str): URL from which proxies will be collected
      page-count (int): count of pages to collect
      check-to-validity (bool): flag which responsible for proxy validation 
Response:
  headers:
    Content-Type: application/json
  body:
    JSON-object of the following format: 
      {
          "status": "ok",
          "data": {
              "proxies": [
                  ...
              ]
          },
          "errors": []
      }
```

## Example
```bash
# build image by Dockerfile
docker build -t gatherproxy-parser-web-service .
# run container by image
docker run -ti -p 8080:80 gatherproxy-parser-web-service
# make curl request to endpoint
curl -d '{"url-to-parse": "http://www.gatherproxy.com/proxylist/country/?c=Russia", "page-count": 5, "check-to-validity": true}' -H "Content-Type: application/json" -X POST http://localhost:8080/api/v1/proxy-collector/collect

```

## TODO:
 - add asynchronus gunicorn worker and nginx
 - migrate to uvloop
 - migrate to aiologger
 - add UML diagram
 
## [Trello board](https://trello.com/b/GbXc8njy/gatherproxy-parser)
