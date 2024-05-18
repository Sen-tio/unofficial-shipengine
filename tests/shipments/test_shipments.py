import unittest
import os

from vcr_unittest import VCRTestCase
from pathlib import Path
from dotenv import load_dotenv

from src.unofficial_shipengine.common.models import Address, Package, Weight
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError

from src.unofficial_shipengine.shipments.models import (
    ShipmentRequest,
    Shipment,
    AdvancedOptions,
)
from src.unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

load_dotenv()

BASE_DIR: Path = Path(__file__).parent


class TestShipments(VCRTestCase):

    def _get_vcr(self, **kwargs):
        vcr = super(TestShipments, self)._get_vcr(**kwargs)
        vcr.filter_headers = ["API-Key"]
        vcr.cassette_library_dir = (BASE_DIR / "vcr_cassettes").as_posix()
        return vcr

    def setUp(self) -> None:
        super(TestShipments, self).setUp()
        self.api_key = os.getenv("SHIPENGINE_API_KEY")
        self.client = UnofficialShipEngine(api_key=self.api_key)

        carriers = self.client.carriers.get_carriers()[0]

        self.shipment_request: ShipmentRequest = ShipmentRequest(
            carrier_id=carriers.carrier_id,
            service_code="usps_ground_advantage",
            ship_to=Address(
                name="Electronic Output Solutions",
                phone="555-555-5555",
                address_line1="2510 Commerce Way",
                city_locality="Vista",
                state_province="CA",
                postal_code="92081",
                country_code="US",
            ),
            ship_from=Address(
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

    def test_create_single_shipment_success(self):
        shipment = self.client.shipments.create_shipment(self.shipment_request)

        self.assertIsInstance(shipment, Shipment)
        self.assertIsInstance(shipment.ship_to, Address)
        self.assertIsInstance(shipment.ship_from, Address)
        self.assertIsInstance(shipment.packages, list)
        self.assertTrue(all(isinstance(obj, Package) for obj in shipment.packages))
        self.assertIsInstance(shipment.advanced_options, AdvancedOptions)
        self.assertIsInstance(shipment.total_weight, Weight)
        self.assertIsInstance(shipment.return_to, Address)

    def test_create_multiple_shipment_success(self):
        shipments = self.client.shipments.create_shipment([self.shipment_request] * 2)

        self.assertIsInstance(shipments, list)
        self.assertTrue(all(isinstance(obj, Shipment) for obj in shipments))

    def test_create_shipment_failure(self):
        self.shipment_request.carrier_id = "bad-carrier-id"

        self.assertRaises(
            ShipEngineAPIError,
            self.client.shipments.create_shipment,
            self.shipment_request,
        )


if __name__ == "__main__":
    unittest.main()
