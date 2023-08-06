import pytest
import json

from test import test_data

from test.fixtures import *
from exchange.services import RestService


@pytest.fixture
def services(rest_service: RestService):
    return [rest_service]


async def test_rest(test_client: TestClient, rest_service: RestService):
    rest_service.context['data'] = test_data
    response = await test_client.get('/')
    response_data = await response.json()
    assert response.status == 200
    data = json.loads(test_data)
    assert data == response_data


async def test_rest_fail(test_client: TestClient):
    response = await test_client.get('/')
    assert response.status == 400
    response_data = await response.json()
    assert {"rates": "No data"} == response_data
