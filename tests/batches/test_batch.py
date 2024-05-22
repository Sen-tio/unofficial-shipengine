import pytest
from pathlib import Path


from unofficial_shipengine.exceptions import ShipEngineAPIError
from unofficial_shipengine.core.batches.models import Batch, BatchRequest, ProcessLabels

BASE_DIR: Path = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return (BASE_DIR / "vcr_cassettes").as_posix()


@pytest.mark.vcr
def test_get_by_id_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])
    created_batch = client.batches.create_batch(batch_request)
    batch = client.batches.get_by_id(created_batch.batch_id)

    assert batch.batch_id == created_batch.batch_id


@pytest.mark.vcr
def test_get_by_id_fail(client):
    with pytest.raises(ShipEngineAPIError):
        client.batches.get_by_id("bad-batch-id")


@pytest.mark.vcr
def test_add_to_batch_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])

    batch = client.batches.create_batch(batch_request)
    before_count = batch.count

    new_shipment = client.shipments.create_shipment(shipment_request)
    client.batches.add_to_batch(batch, shipments=[new_shipment])

    batch = client.batches.get_by_id(batch.batch_id)

    assert batch.count == before_count + 1


@pytest.mark.vcr
def test_add_to_batch_fail(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])

    batch = client.batches.create_batch(batch_request)

    with pytest.raises(ShipEngineAPIError):
        client.batches.add_to_batch(batch, shipments=["bad-shipment-id"])


@pytest.mark.vcr
def test_remove_from_batch_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])

    batch = client.batches.create_batch(batch_request)
    before_count = batch.count

    client.batches.remove_from_batch(batch, shipments=[shipment])

    batch = client.batches.get_by_id(batch.batch_id)

    assert batch.count == before_count - 1


@pytest.mark.vcr
def test_remove_from_batch_fail(client):
    with pytest.raises(ShipEngineAPIError):
        client.batches.remove_from_batch("bad-batch-id", shipments=["bad-batch-id"])


@pytest.mark.vcr
def test_create_batch_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])
    batch = client.batches.create_batch(batch_request)

    assert batch.status == batch.Status.OPEN.value


@pytest.mark.vcr
def test_create_batch_fail(client):
    batch_request = BatchRequest(shipment_ids=["bad-shipment-id"])
    with pytest.raises(ShipEngineAPIError):
        client.batches.create_batch(batch_request)


@pytest.mark.vcr
def test_delete_batch_success(client, shipment_request):
    shipment_request = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment_request.shipment_id])
    batch = client.batches.create_batch(batch_request)
    client.batches.delete_batch(batch)
    batch = client.batches.get_by_id(batch.batch_id)

    assert batch.status == batch.Status.ARCHIVED.value


@pytest.mark.vcr
def test_delete_batch_fail(client):
    with pytest.raises(ShipEngineAPIError):
        client.batches.delete_batch("bad-batch-id")


@pytest.mark.vcr
def test_process_labels_success(client, shipment_request):
    shipment = client.shipments.create_shipment(shipment_request)
    batch_request = BatchRequest(shipment_ids=[shipment.shipment_id])
    batch = client.batches.create_batch(batch_request)
    client.batches.process_labels(batch, process_labels=ProcessLabels())

    batch = client.batches.get_by_id(batch.batch_id)

    assert batch.status in [
        Batch.Status.QUEUED.value,
        Batch.Status.PROCESSING.value,
        Batch.Status.COMPLETED.value,
        Batch.Status.COMPLETED_WITH_ERRORS.value,
    ]


@pytest.mark.vcr
def test_process_labels_fail(client):
    with pytest.raises(ShipEngineAPIError):
        client.batches.process_labels("bad-batch-id", process_labels=ProcessLabels())
