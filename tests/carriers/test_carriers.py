from pathlib import Path

import pytest
from dotenv import load_dotenv

from unofficial_shipengine.carriers.models import Carrier
from unofficial_shipengine.core.exceptions import ShipEngineAPIError

load_dotenv()

BASE_DIR: Path = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_get_carriers(client) -> None:
    carriers: list[Carrier] = client.carriers.get_carriers()

    assert isinstance(carriers, list)
    assert all(isinstance(obj, Carrier) for obj in carriers)


@pytest.mark.vcr
def test_get_by_id_success(client) -> None:
    carriers: list[Carrier] = client.carriers.get_carriers()
    carrier_to_get: Carrier = carriers[0]
    carrier: Carrier = client.carriers.get_by_id(carrier_to_get.carrier_id)

    assert carrier.carrier_id == carrier_to_get.carrier_id


@pytest.mark.vcr
def test_get_by_id_fail(client) -> None:
    with pytest.raises(ShipEngineAPIError):
        client.carriers.get_by_id("bad-carrier-id")
