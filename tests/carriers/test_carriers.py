import unittest

from vcr_unittest import VCRTestCase
from pathlib import Path

from src.unofficial_shipengine.core.carriers import Carrier
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError

BASE_DIR: Path = Path(__file__).parent


class TestCarriers(VCRTestCase):

    def _get_vcr(self, **kwargs):
        vcr = super(TestCarriers, self)._get_vcr(**kwargs)
        vcr.filter_headers = ["API-Key"]
        vcr.cassette_library_dir = (BASE_DIR / "vcr_cassettes").as_posix()
        return vcr

    def setUp(self) -> None:
        super(TestCarriers, self).setUp()

    def test_get_carriers(self) -> None:
        carriers: list[Carrier] = Carrier.get_carriers()

        self.assertIsInstance(carriers, list)
        self.assertTrue(all(isinstance(obj, Carrier) for obj in carriers))

    def test_get_by_id_success(self) -> None:
        carriers: list[Carrier] = Carrier.get_carriers()
        carrier_to_get: Carrier = carriers[0]
        carrier: Carrier = Carrier.get_by_id(carrier_to_get.carrier_id)

        self.assertEqual(carrier.carrier_id, carrier_to_get.carrier_id)

    def test_get_by_id_fail(self) -> None:
        self.assertRaises(ShipEngineAPIError, Carrier.get_by_id, "bad-carrier-id")


if __name__ == "__main__":
    unittest.main()
