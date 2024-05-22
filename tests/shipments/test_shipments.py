import pytest
from pathlib import Path
from dotenv import load_dotenv

from unofficial_shipengine.core.common.models import Address, Package, Weight
from unofficial_shipengine.exceptions import ShipEngineAPIError

from unofficial_shipengine.core.shipments.models import (
    Shipment,
    AdvancedOptions,
)

load_dotenv()

BASE_DIR: Path = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_create_single_shipment_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)

    assert isinstance(shipment, Shipment)
    assert isinstance(shipment.ship_to, Address)
    assert isinstance(shipment.ship_from, Address)
    assert isinstance(shipment.packages, list)
    assert all(isinstance(obj, Package) for obj in shipment.packages)
    assert isinstance(shipment.advanced_options, AdvancedOptions)
    assert isinstance(shipment.total_weight, Weight)
    assert isinstance(shipment.return_to, Address)


@pytest.mark.vcr
def test_create_multiple_shipment_success(client, shipment_request):
    shipments = client.shipments.create_shipment([shipment_request] * 2)

    assert isinstance(shipments, list)
    assert all(isinstance(obj, Shipment) for obj in shipments)


@pytest.mark.vcr
def test_create_shipment_failure(client, shipment_request):
    shipment_request.carrier_id = "bad-carrier-id"

    with pytest.raises(ShipEngineAPIError):
        client.shipments.create_shipment(shipment_request)


# TODO: finish writing tests
