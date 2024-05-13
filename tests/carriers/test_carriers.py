import unittest
from pathlib import Path

from vcr_unittest import VCRTestCase

from src.unofficial_shipengine.core.carriers import Carrier

BASE_DIR: Path = Path(__file__).parent


class TestBatch(VCRTestCase):

    def _get_vcr(self, **kwargs):
        vcr = super(TestBatch, self)._get_vcr(**kwargs)
        vcr.filter_headers = ["API-Key"]
        vcr.cassette_library_dir = (BASE_DIR / "vcr_cassettes").as_posix()
        return vcr

    def setUp(self):
        super(TestBatch, self).setUp()

    def test_get_by_id_success(self):
        carrier = Carrier.get_by_id("se-64525")

        self.assertEqual(carrier.carrier_id, "se-64525")


if __name__ == "__main__":
    unittest.main()
