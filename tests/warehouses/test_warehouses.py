from pathlib import Path

import pytest

from unofficial_shipengine.warehouses.models import Warehouse
from unofficial_shipengine.core.exceptions import ShipEngineAPIError

BASE_DIR = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_create_warehouse_success(client, warehouse_request):
    warehouse = client.warehouses.create_warehouse(warehouse_request)

    assert isinstance(warehouse, Warehouse)


@pytest.mark.vcr
def test_create_warehouse_failure(client, warehouse_request):
    with pytest.raises(ShipEngineAPIError):
        warehouse_request.origin_address.address_line1 = ""
        client.warehouses.create_warehouse(warehouse_request)


@pytest.mark.vcr
def test_delete_warehouse_success(client, warehouse_request):
    warehouse = client.warehouses.create_warehouse(warehouse_request)
    client.warehouses.delete_warehouse(warehouse)

    with pytest.raises(ShipEngineAPIError):
        client.warehouses.get_by_id(warehouse.warehouse_id)


@pytest.mark.vcr
def test_delete_warehouse_failure(client, warehouse_request):
    with pytest.raises(ShipEngineAPIError):
        client.warehouses.delete_warehouse("bad-warehouse-id")


@pytest.mark.vcr
def test_get_by_id_success(client, warehouse_request):
    created_warehouse = client.warehouses.create_warehouse(warehouse_request)
    warehouse = client.warehouses.get_by_id(created_warehouse.warehouse_id)

    assert isinstance(warehouse, Warehouse)


@pytest.mark.vcr
def test_get_by_id_failure(client):
    with pytest.raises(ShipEngineAPIError):
        client.warehouses.get_by_id("bad-warehouse-id")
