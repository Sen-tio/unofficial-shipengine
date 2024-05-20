import pytest
import os
import vcr

from typing import Generator
from dotenv import load_dotenv
from pathlib import Path

from unofficial_shipengine.shipments.models import ShipmentRequest
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine
from unofficial_shipengine.common.models import Address, Package, Weight
from unofficial_shipengine.warehouses.models import WarehouseRequest, Warehouse

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": ["API-Key"]}


@pytest.fixture(scope="session")
def client():
    api_key = os.getenv("SHIPENGINE_API_KEY", "")
    return UnofficialShipEngine(api_key)


@pytest.fixture(scope="function")
def warehouse_request():
    return WarehouseRequest(
        name="Test Warehouse 123",
        origin_address=Address(
            name="Electronic Output Solutions",
            phone="555-555-5555",
            address_line1="2510 Commerce Way",
            city_locality="Vista",
            state_province="CA",
            postal_code="92081",
            country_code="US",
        ),
    )


@pytest.fixture(scope="function")
def warehouse(client, warehouse_request) -> Generator:
    warehouse: Warehouse = client.warehouses.create_warehouse(warehouse_request)
    yield warehouse
    client.warehouses.delete_warehouse(warehouse)


@pytest.fixture(scope="function")
def shipment_request(client, warehouse):
    with vcr.use_cassette(
        BASE_DIR / "vcr_cassettes" / "shipment_request.yaml", filter_headers=["API-Key"]
    ):
        carriers = client.carriers.get_carriers()[0]

    return ShipmentRequest(
        carrier_id=carriers.carrier_id,
        service_code="usps_ground_advantage",
        warehouse_id=warehouse.warehouse_id,
        ship_to=Address(
            name="Electronic Output Solutions",
            phone="555-555-5555",
            address_line1="2510 Commerce Way",
            city_locality="Vista",
            state_province="CA",
            postal_code="92081",
            country_code="US",
        ),
        packages=[Package(Weight(1, Weight.Unit.OUNCE))],
    )
