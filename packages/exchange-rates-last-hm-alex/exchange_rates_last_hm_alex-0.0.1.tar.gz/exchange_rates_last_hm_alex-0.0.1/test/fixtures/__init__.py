import pytest
from aiohttp.test_utils import TestClient, TestServer
from aiohttp.web_app import Application
from aiomisc_pytest.pytest_plugin import aiomisc_unused_port

from exchange.services import RestService, ExchangeRatesUpdater


@pytest.fixture
def rest_service(aiomisc_unused_port):
    return RestService(host='0.0.0.0', port=aiomisc_unused_port)


@pytest.fixture
def updater_service():
    return ExchangeRatesUpdater(interval=30)


@pytest.fixture
def app(services):
    return services[0].app


@pytest.fixture
async def test_client(app: Application, aiomisc_unused_port, loop):
    test_server = TestServer(app, loop=loop)
    await test_server.start_server(loop=loop)
    test_client = TestClient(test_server)
    try:
        yield test_client
    finally:
        await test_client.close()