from test.fixtures import *


@pytest.fixture
def services(rest_service, updater_service):
    return [rest_service, updater_service]


async def test_rest_service(test_client: TestClient, updater_service: ExchangeRatesUpdater):
    await updater_service.callback()
    response = await test_client.get('/')
    assert response.status == 200
    data = await response.json()
    assert 'rates' in data.keys()
    assert 'base' in data.keys()
    assert 'date' in data.keys()
