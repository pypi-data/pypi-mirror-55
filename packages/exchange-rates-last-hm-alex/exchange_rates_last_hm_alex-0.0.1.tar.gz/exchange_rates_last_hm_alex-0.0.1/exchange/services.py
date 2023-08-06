import errno
import logging

import aiohttp
from aiohttp.abc import Application
from aiomisc.service.periodic import PeriodicService
from aiomisc.service.aiohttp import AIOHTTPService
from aiomisc.backoff import asyncbackoff
from aiohttp import web
from asyncio import TimeoutError

log = logging.getLogger(__name__)
url = 'https://api.ratesapi.io/api/latest'


class RestService(AIOHTTPService):

    async def create_application(self) -> Application:
        self.app = web.Application()
        self.app.add_routes(
            [
                web.get('/', handler=self.handler)
            ]
        )
        return self.app

    async def handler(self, request):
        try:
            result = await self._get_data_from_context()
        except TimeoutError as e:
            log.error('Timeout during get data from context. Bad request produced. Exception info - %s', e)
            if self.context['data'].cancelled():
                del self.context._storage['data']
            return web.Response(text='{"rates":"No data"}', status=400, content_type='application/json')
        log.info('Returning data: %s', result)
        return web.Response(text=result, content_type='application/json')

    @asyncbackoff(0.1, 1, 0.1)
    async def _get_data_from_context(self):
        result = await self.context['data']
        return result


class ExchangeRatesUpdater(PeriodicService):

    async def start(self):
        self.session = aiohttp.ClientSession()
        log.info("Setup session pool for %s service", self)
        await super().start()

    async def callback(self):
        a = await self._get_data()
        if a:
            self.context['data'] = a

    @asyncbackoff(attempt_timeout=0.2,
                  deadline=None, pause=0.2,
                  max_tries=3,
                  exceptions=[OSError],
                  giveup=lambda e: type(e) is OSError and (e.errno != errno.ECONNABORTED))
    async def _get_data(self):
        log.debug('Make a request to %s to update exchange rates', url)
        async with self.session.get(url=url) as resp:
            log.info('Request to [%s] ended, status - %d', resp.request_info.url, resp.status)
            text = await resp.text()
            log.debug('%s response\nheaders: %s\nbody :%s', resp.request_info.url, resp.headers, text)
            if resp.status == 200:
                return text

    async def stop(self, err):
        await super().stop(err)
        await self.session.close()
        log.info("Close session pool for %s service", self)
