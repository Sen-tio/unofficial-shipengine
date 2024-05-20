import unittest
import os
import pytest
from pathlib import Path

from vcr_unittest import VCRTestCase

from unofficial_shipengine.common.models import Address, Package, Weight
from unofficial_shipengine.core.exceptions import ShipEngineAPIError
from unofficial_shipengine.shipments.models import Shipment, ShipmentRequest
from unofficial_shipengine.batches.models import Batch, BatchRequest, ProcessLabels
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

BASE_DIR: Path = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


def test_get_by_id_success(client, batch_request):
    created_batch: Batch = client.batches.create_batch(batch_request)
    batch: Batch = client.batches.get_by_id(created_batch.batch_id)

    assert batch.batch_id == created_batch.batch_id


def test_get_by_id_fail(client):
    with pytest.raises(ShipEngineAPIError):
        client.batches.get_by_id("bad-batch-id")


def test_add_to_batch_success(client, batch_request, shipment_request):
    batch: Batch = client.batches.create_batch(batch_request)
    before_count: int = batch.count

    new_shipment = client.shipments.create_shipment(shipment_request)
    client.batches.add_to_batch(batch, shipment_ids=[new_shipment.shipment_id])

    batch: Batch = client.batches.get_by_id(batch.batch_id)

    assert batch.count == before_count + 1


def test_add_to_batch_fail(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)

    with pytest.raises(ShipEngineAPIError):
        client.batches.add_to_batch(batch, shipment_ids=["bad-shipment-id"])


def test_remove_from_batch_success(client, batch_request, shipment):
    batch: Batch = client.batches.create_batch(batch_request)
    before_count: int = batch.count

    client.batches.remove_from_batch(batch, shipment_ids=[shipment.shipment_id])

    batch: Batch = client.batches.get_by_id(batch.batch_id)

    assert batch.count == before_count - 1


def test_remove_from_batch_fail(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)

    with pytest.raises(ShipEngineAPIError):
        client.batches.remove_from_batch(batch, shipment_ids=["bad-shipment-id"])


def test_create_batch_success(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)

    assert batch.status == batch.Status.OPEN.value


def test_create_batch_fail(client, batch_request):
    batch_request.shipment_ids = ["bad-shipment-id"]

    with pytest.raises(ShipEngineAPIError):
        client.batches.create_batch(batch_request)


def test_delete_batch_success(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)
    client.batches.delete_batch(batch)
    batch = client.batches.get_by_id(batch.batch_id)

    assert batch.status == batch.Status.ARCHIVED.value


def test_delete_batch_fail(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)
    batch.batch_id = "bad-batch-id"

    with pytest.raises(ShipEngineAPIError):
        client.batches.delete_batch(batch)


def test_process_labels_success(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)
    client.batches.process_labels(batch, process_labels=ProcessLabels())

    batch: Batch = client.batches.get_by_id(batch.batch_id)

    assert batch.status in [
        Batch.Status.QUEUED.value,
        Batch.Status.PROCESSING.value,
        Batch.Status.COMPLETED.value,
        Batch.Status.COMPLETED_WITH_ERRORS.value,
    ]


def test_process_labels_fail(client, batch_request):
    batch: Batch = client.batches.create_batch(batch_request)
    batch.batch_id = "bad-batch-id"

    with pytest.raises(ShipEngineAPIError):
        client.batches.process_labels(batch, process_labels=ProcessLabels())

    # TODO: Finish building out batches nodule
