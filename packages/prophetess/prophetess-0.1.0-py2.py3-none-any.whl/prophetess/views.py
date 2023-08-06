import logging

from aiohttp import web

from prophetess import utils
from prophetess import config

log = logging.getLogger(__name__)


class ApiView(web.View):

    async def get(self):
        uri = [el for el in self.request.match_info.get('uri', '').split('/') if el]

        log.debug(uri)

        if not uri:
            raise web.HTTPNotFound(text='Invalid Resource')

        data = await self.shake_tree(uri, config.tree)
        if data:
            return web.json_response(data)

        raise web.HTTPNotFound(text='No matching records')


class MetricsView(web.View):

    async def get(self):
        return web.json_response({'soon'})
