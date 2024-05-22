import pytest
from dotenv import load_dotenv
from pathlib import Path

from unofficial_shipengine.core.tracking.models import TrackingInformation
from unofficial_shipengine.exceptions import ShipEngineAPIError

load_dotenv()

BASE_DIR: Path = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_get_tracking_information_success(client, label_request):
    label = client.labels.purchase_label(label_request)
    tracking_info = client.tracking.get_tracking_information(
        label.carrier_code, label.tracking_number
    )

    assert isinstance(tracking_info, TrackingInformation)


@pytest.mark.vcr
def test_get_tracking_information_failure(client):
    with pytest.raises(ShipEngineAPIError):
        client.tracking.get_tracking_information("bad-carrier-code", "")


@pytest.mark.vcr
def test_start_tracking_package_success(client, label_request):
    label = client.labels.purchase_label(label_request)
    client.tracking.start_tracking_package(label.carrier_code, label.tracking_number)


@pytest.mark.vcr
def test_stop_tracking_package_success(client, label_request):
    label = client.labels.purchase_label(label_request)
    client.tracking.stop_tracking_package(label.carrier_code, label.tracking_number)


@pytest.mark.vcr
def test_tracking_package_failure(client, label_request):
    with pytest.raises(ShipEngineAPIError):
        client.tracking.start_tracking_package("bad-carrier-code", "")
