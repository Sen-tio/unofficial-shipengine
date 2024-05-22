from pathlib import Path

import pytest

from unofficial_shipengine.core.tracking.models import TrackingInformation
from unofficial_shipengine.core.labels.models import Label
from unofficial_shipengine.exceptions import ShipEngineAPIError

BASE_DIR = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_purchase_label_success(client, label_request) -> None:
    label = client.labels.purchase_label(label_request)

    assert isinstance(label, Label)
    assert label.status == Label.Status.COMPLETED.value


@pytest.mark.vcr
def test_purchase_label_fail(client, label_request) -> None:
    with pytest.raises(ShipEngineAPIError):
        label_request.shipment = "bad-shipment-data"
        client.labels.purchase_label(label_request)


@pytest.mark.vcr
def test_create_return_label_success(
    client, label_request, return_label_request
) -> None:
    label = client.labels.purchase_label(label_request)
    return_label = client.labels.create_return_label(label, return_label_request)

    assert isinstance(return_label, Label)


@pytest.mark.vcr
def test_create_return_label_fail(client, label_request) -> None:
    with pytest.raises(ShipEngineAPIError):
        label_request.shipment = "bad-shipment-data"
        client.labels.create_return_label("bad-label-id", label_request)


@pytest.mark.vcr
def test_get_by_id_success(client, label_request) -> None:
    created_label = client.labels.purchase_label(label_request)
    label = client.labels.get_by_id(created_label.label_id)

    assert isinstance(label, Label)


@pytest.mark.vcr
def test_get_by_id_fail(client) -> None:
    with pytest.raises(ShipEngineAPIError):
        client.labels.get_by_id("bad-label-id")


@pytest.mark.vcr
def test_get_label_tracking_information_success(client, label_request) -> None:
    label = client.labels.purchase_label(label_request)
    label_tracking_information = client.labels.get_label_tracking_info(label)

    assert isinstance(label_tracking_information, TrackingInformation)


@pytest.mark.vcr
def test_get_label_tracking_information_failure(client, label_request) -> None:
    with pytest.raises(ShipEngineAPIError):
        client.labels.get_label_tracking_info("bad-label-id")
