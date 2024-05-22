import pytest
from pathlib import Path
from dotenv import load_dotenv

from datetime import datetime
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


@pytest.mark.vcr
def test_get_by_id_success(client, shipment_request):
    created_shipment = client.shipments.create_shipment(shipment_request)
    shipment = client.shipments.get_by_id(created_shipment.shipment_id)

    assert isinstance(shipment, Shipment)


@pytest.mark.vcr
def test_get_by_id_failure(client):
    with pytest.raises(ShipEngineAPIError):
        client.shipments.get_by_id("bad-shipment-id")


@pytest.mark.vcr
def test_get_by_external_id_success(client, shipment_request):
    shipment_request.external_shipment_id = f"{datetime.now():%Y%m%d%H%M%S}"
    created_shipment = client.shipments.create_shipment(shipment_request)
    shipment = client.shipments.get_by_external_id(
        created_shipment.external_shipment_id
    )

    assert isinstance(shipment, Shipment)


@pytest.mark.vcr
def test_get_by_external_id_failure(client):
    with pytest.raises(ShipEngineAPIError):
        client.shipments.get_by_external_id("some-non-existing-external-id")


@pytest.mark.vcr
def test_update_shipment_success(client, shipment_request):
    name_to_change_to = "New Name"
    shipment = client.shipments.create_shipment(shipment_request)
    shipment.ship_to.name = name_to_change_to
    client.shipments.update_shipment(shipment)
    shipment = client.shipments.get_by_id(shipment.shipment_id)

    assert shipment.ship_to.name == name_to_change_to


@pytest.mark.vcr
def test_update_shipment_failure(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    shipment.shipment_id = "bad-shipment-id"

    with pytest.raises(ShipEngineAPIError):
        client.shipments.update_shipment(shipment)


@pytest.mark.vcr
def test_cancel_shipment_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    client.shipments.cancel_shipment(shipment)
    shipment = client.shipments.get_by_id(shipment.shipment_id)

    assert shipment.shipment_status == Shipment.Status.CANCELLED.value


@pytest.mark.vcr
def test_cancel_shipment_failure(client):
    with pytest.raises(ShipEngineAPIError):
        client.shipments.cancel_shipment("bad-shipment-id")
