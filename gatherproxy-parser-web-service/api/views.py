from aiohttp import web
from .forms import CollectRequestSchema


class CollectRequestHandler:
    def __init__(self):
        pass

    async def health(self, request: web.Request) -> web.Response:
        return web.Response(body="OK")

    async def swagger(self, request: web.Request) -> web.Response:
        return web.Response(body="OK")

    async def collect(self, request: web.Request) -> web.Response:
        post_data = await request.text()
        print(post_data)
        form = CollectRequestSchema().loads(post_data)
        print(form)

        return web.Response(body="OK")
