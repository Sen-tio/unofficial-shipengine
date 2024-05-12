import unittest
import vcr

from src.unofficial_shipengine.core.common import Address, Package, Weight
from src.unofficial_shipengine.core.shipment import ShipmentRequest, Shipment
from src.unofficial_shipengine.core.batches import Batch, BatchRequest, ProcessLabels
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError


# TODO: refactor tests to reuse a batch created in setup with a shipment
class TestBatch(unittest.TestCase):
    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_get_by_id_success(self):
        batch: Batch = Batch.get_by_id("se-1038286")

        self.assertEqual(batch.batch_id, "se-1038286")

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_get_by_id_fail(self):
        self.assertRaises(ShipEngineAPIError, Batch.get_by_id, "bad-batch-id")

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_add_to_batch_success(self):
        shipment_request: ShipmentRequest = ShipmentRequest(
            carrier_id="se-64525",
            warehouse_id="se-18511",
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
        shipment: Shipment = Shipment.create_shipment(shipment_request)

        batch: Batch = Batch.create_batch(BatchRequest([shipment.shipment_id]))
        before_count: int = batch.count

        batch.add_to_batch([Shipment.create_shipment(shipment_request).shipment_id])

        batch: Batch = Batch.get_by_id(batch.batch_id)

        self.assertEqual(batch.count, before_count + 1)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_add_to_batch_fail(self):
        batch: Batch = Batch.get_by_id("se-1038286")

        self.assertRaises(ShipEngineAPIError, batch.add_to_batch, ["bad-batch-id"])

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_remove_from_batch_success(self):
        shipment_request: ShipmentRequest = ShipmentRequest(
            carrier_id="se-64525",
            warehouse_id="se-18511",
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
        shipment: Shipment = Shipment.create_shipment(shipment_request)

        batch: Batch = Batch.create_batch(BatchRequest([shipment.shipment_id]))
        before_count: int = batch.count

        batch.remove_from_batch([shipment.shipment_id])
        batch: Batch = Batch.get_by_id(batch.batch_id)

        self.assertEqual(batch.count, before_count - 1)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_remove_from_batch_fail(self):
        batch: Batch = Batch.get_by_id("se-1038286")

        self.assertRaises(ShipEngineAPIError, batch.remove_from_batch, ["bad-batch-id"])

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_create_batch_success(self):
        batch_request: BatchRequest = BatchRequest(
            shipment_ids=["se-1518508", "se-1519477"]
        )

        batch: Batch = Batch.create_batch(batch_request)

        self.assertEqual(batch.status, batch.Status.OPEN.value)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_create_batch_fail(self):
        batch_request: BatchRequest = BatchRequest(shipment_ids=["se-1223"])

        self.assertRaises(ShipEngineAPIError, Batch.create_batch, batch_request)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_delete_batch_success(self):
        batch_request: BatchRequest = BatchRequest(
            shipment_ids=["se-1518508", "se-1519477"]
        )

        batch: Batch = Batch.create_batch(batch_request)
        batch.delete_batch()
        batch = batch.get_by_id(batch.batch_id)

        self.assertEqual(batch.status, batch.Status.ARCHIVED.value)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_delete_batch_fail(self):
        batch_request: BatchRequest = BatchRequest(shipment_ids=["se-1518508"])

        batch: Batch = Batch.create_batch(batch_request)
        batch.batch_id = "bad-batch-id"

        self.assertRaises(ShipEngineAPIError, batch.delete_batch)

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_process_labels_success(self):
        batch_request: BatchRequest = BatchRequest(
            shipment_ids=["se-1518508", "se-1519477"]
        )

        batch: Batch = Batch.create_batch(batch_request)
        batch.process_labels(process_labels=ProcessLabels())

        batch: Batch = Batch.get_by_id(batch.batch_id)

        self.assertIn(
            batch.status,
            [
                Batch.Status.QUEUED.value,
                Batch.Status.PROCESSING.value,
                Batch.Status.COMPLETED.value,
                Batch.Status.COMPLETED_WITH_ERRORS.value,
            ],
        )

    @vcr.use_cassette(cassette_library_dir="vcr_cassettes", filter_headers=["API-Key"])
    def test_process_labels_fail(self):
        batch_request: BatchRequest = BatchRequest(
            shipment_ids=["se-1518508", "se-1519477"]
        )

        batch: Batch = Batch.create_batch(batch_request)
        batch.batch_id = "bad-batch-id"

        self.assertRaises(
            ShipEngineAPIError, batch.process_labels, process_labels=ProcessLabels()
        )


if __name__ == "__main__":
    unittest.main()
