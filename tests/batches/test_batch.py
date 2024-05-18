import unittest
import os
from pathlib import Path

from vcr_unittest import VCRTestCase

from src.unofficial_shipengine.common.models import Address, Package, Weight
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError
from src.unofficial_shipengine.shipments.models import Shipment, ShipmentRequest
from src.unofficial_shipengine.batches.models import Batch, BatchRequest, ProcessLabels
from src.unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

BASE_DIR: Path = Path(__file__).parent


class TestBatch(VCRTestCase):

    def _get_vcr(self, **kwargs):
        vcr = super(TestBatch, self)._get_vcr(**kwargs)
        vcr.filter_headers = ["API-Key"]
        vcr.cassette_library_dir = (BASE_DIR / "vcr_cassettes").as_posix()
        return vcr

    def setUp(self):
        super(TestBatch, self).setUp()
        self.api_key = os.getenv("SHIPENGINE_API_KEY")
        self.client = UnofficialShipEngine(api_key=self.api_key)
        self.shipment_request: ShipmentRequest = ShipmentRequest(
            carrier_id="se-64525",  # TODO: alter this as to make it reusable for another person
            warehouse_id="se-18511",  # TODO: alter this as to make it reusable for another person
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
            packages=[Package(Weight(1, Weight.Unit.OUNCE))],
        )

        self.shipment: Shipment = self.client.shipments.create_shipment(
            self.shipment_request
        )

        self.batch_request: BatchRequest = BatchRequest(
            shipment_ids=[self.shipment.shipment_id]
        )

    def test_get_by_id_success(self):
        created_batch: Batch = self.client.batches.create_batch(self.batch_request)
        batch: Batch = self.client.batches.get_by_id(created_batch.batch_id)

        self.assertEqual(batch.batch_id, created_batch.batch_id)

    def test_get_by_id_fail(self):
        self.assertRaises(
            ShipEngineAPIError, self.client.batches.get_by_id, "bad-batch-id"
        )

    def test_add_to_batch_success(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        before_count: int = batch.count

        new_shipment = self.client.shipments.create_shipment(self.shipment_request)
        self.client.batches.add_to_batch(batch, shipment_ids=[new_shipment.shipment_id])

        batch: Batch = self.client.batches.get_by_id(batch.batch_id)

        self.assertEqual(batch.count, before_count + 1)

    def test_add_to_batch_fail(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)

        self.assertRaises(
            ShipEngineAPIError,
            self.client.batches.add_to_batch,
            batch,
            ["bad-batch-id"],
        )

    def test_remove_from_batch_success(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        before_count: int = batch.count

        self.client.batches.remove_from_batch(
            batch, shipment_ids=[self.shipment.shipment_id]
        )

        batch: Batch = self.client.batches.get_by_id(batch.batch_id)

        self.assertEqual(batch.count, before_count - 1)

    def test_remove_from_batch_fail(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)

        self.assertRaises(
            ShipEngineAPIError,
            self.client.batches.remove_from_batch,
            batch,
            ["bad-batch-id"],
        )

    def test_create_batch_success(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)

        self.assertEqual(batch.status, batch.Status.OPEN.value)

    def test_create_batch_fail(self):
        self.batch_request.shipment_ids = ["bad-shipment-id"]

        self.assertRaises(
            ShipEngineAPIError, self.client.batches.create_batch, self.batch_request
        )

    def test_delete_batch_success(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        self.client.batches.delete_batch(batch)
        batch = self.client.batches.get_by_id(batch.batch_id)

        self.assertEqual(batch.status, batch.Status.ARCHIVED.value)

    def test_delete_batch_fail(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        batch.batch_id = "bad-batch-id"

        self.assertRaises(ShipEngineAPIError, self.client.batches.delete_batch, batch)

    def test_process_labels_success(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        self.client.batches.process_labels(batch, process_labels=ProcessLabels())

        batch: Batch = self.client.batches.get_by_id(batch.batch_id)

        self.assertIn(
            batch.status,
            [
                Batch.Status.QUEUED.value,
                Batch.Status.PROCESSING.value,
                Batch.Status.COMPLETED.value,
                Batch.Status.COMPLETED_WITH_ERRORS.value,
            ],
        )

    def test_process_labels_fail(self):
        batch: Batch = self.client.batches.create_batch(self.batch_request)
        batch.batch_id = "bad-batch-id"

        self.assertRaises(
            ShipEngineAPIError,
            self.client.batches.process_labels,
            batch=batch,
            process_labels=ProcessLabels(),
        )

        # TODO: Finish building out batches nodule


if __name__ == "__main__":
    unittest.main()
