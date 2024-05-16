import unittest

from vcr_unittest import VCRTestCase
from pathlib import Path

from src.unofficial_shipengine.core.shipments import Shipment, ShipmentRequest
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError

BASE_DIR: Path = Path(__file__).parent


class TestShipments(VCRTestCase):

    def _get_vcr(self, **kwargs):
        vcr = super(TestCarriers, self)._get_vcr(**kwargs)
        vcr.filter_headers = ["API-Key"]
        vcr.cassette_library_dir = (BASE_DIR / "vcr_cassettes").as_posix()
        return vcr

    def setUp(self) -> None:
        super(TestCarriers, self).setUp()

    def test_create_shipment_success(self):
        pass


if __name__ == "__main__":
    unittest.main()
