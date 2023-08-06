import pytest
from aioresponses import aioresponses
from exchange.services import url
from test import test_data
from test.fixtures import *


@pytest.fixture
def services(updater_service):
    return [updater_service]


async def test_updater_ok(updater_service: ExchangeRatesUpdater):
    with aioresponses() as mocked:
        mocked.get(url=url, status=200, body=test_data)
        await updater_service.callback()
        context_data = await updater_service.context['data']
        assert context_data == test_data


async def test_updater_fail(updater_service: ExchangeRatesUpdater):
    with aioresponses() as mocked:
        mocked.get(url=url, status=400)
        updated_data = await updater_service._get_data()
        assert updated_data is None