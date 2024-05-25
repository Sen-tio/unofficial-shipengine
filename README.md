# Unofficial Shipengine
The unofficial Python module for ShipEngine API.

![Tests](https://github.com/Sen-tio/unofficial-shipengine/actions/workflows/tests.yml/badge.svg)


The Unofficial ShipEngine client provides a simple interface for interacting with the ShipEngine API. It enables users to manage shipments, carriers, batches, warehouses, labels, and tracking.

## Installation

To install, you can use pip:

```bash
pip install unofficial-shipengine
```

## Usage

### Initialization

```python
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

# Initialize the client with a configuration
client = UnofficialShipEngine(config)
```

### Configuration

The `UnofficialShipEngine` client object requires an API key to communicate with the ShipEngine API. The configuration can be provided in three formats:

1. An instance of `UnofficialShipEngineConfig`:

```python
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine, UnofficialShipEngineConfig

config = UnofficialShipEngineConfig(api_key='your_api_key', retries=3, backoff_factor=0.5)
client = UnofficialShipEngine(config)
```

2. A dictionary containing configuration parameters:

```python
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

config_dict = {
    'api_key': 'your_api_key',
    'retries': 3,
    'backoff_factor': 0.5
}

client = UnofficialShipEngine(config_dict)
```

3. A string representing just the API key (other parameters will default):

```python
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine

client = UnofficialShipEngine("your_api_key")
```

### Services

Once initialized, the client provides access to various services:

- `shipments`: Manage shipments.
- `carriers`: Manage carriers.
- `batches`: Manage batches of shipments.
- `warehouses`: Manage warehouses.
- `labels`: Manage labels for shipments.
- `tracking`: Track shipments.

Example usage:

```python
# Create a shipment
from unofficial_shipengine.unofficial_shipengine import UnofficialShipEngine
from unofficial_shipengine.core.shipments.models import ShipmentRequest
from unofficial_shipengine.core.batches.models import BatchRequest, ProcessLabels

client = UnofficialShipEngine("your_api_key")

shipment_request = ShipmentRequest(...)
shipment = client.shipments.create_shipment(shipment_request)

# Create a batch
batch_request = BatchRequest(...)
batch = client.batches.create_batch(batch_request)

# Add the shipment to the batch
client.batches.add_to_batch(batch, shipments=[shipment])

# Process the batch
client.batches.process_labels(batch, ProcessLabels(...))

# Refetch the batch to either check processing status or download labels
batch = client.batches.get_by_id(batch.batch_id)
```

## Documentation

### ShipmentService

The `ShipmentService` provides methods for interacting with shipment-related endpoints in the ShipEngine API.

#### Methods

- `create_shipment(shipment_request: Union[ShipmentRequest, list[ShipmentRequest]]) -> Union[Shipment, list[Shipment]]`: Creates a shipment or a list of shipments.
- `get_by_id(shipment_id: str) -> Shipment`: Retrieves a shipment by its ID.
- `get_by_external_id(external_shipment_id: str) -> Shipment`: Retrieves a shipment by its external ID.
- `update_shipment(shipment: Shipment) -> Shipment`: Updates an existing shipment.
- `cancel_shipment(shipment: Union[Shipment, str]) -> None`: Cancels a shipment.

### CarrierService

The `CarrierService` provides methods for interacting with carrier-related endpoints in the ShipEngine API.

#### Methods

- `get_carriers() -> list[Carrier]`: Retrieves a list of carriers.
- `get_by_id(carrier_id: str) -> Carrier`: Retrieves a carrier by its ID.
- `add_funds(carrier: Union[Carrier, str], amount: float, currency: str = "usd") -> CarrierBalance`: Adds funds to a carrier account.

### BatchService

The `BatchService` provides methods for interacting with batch-related endpoints in the ShipEngine API.

#### Methods

- `create_batch(batch_shipments: list[str]) -> Batch`: Creates a batch of shipments.
- `get_by_id(batch_id: str) -> Batch`: Retrieves a batch by its ID.
- `add_shipments_to_batch(batch_id: str, shipment_ids: list[str]) -> Batch`: Adds shipments to an existing batch.
- `remove_shipments_from_batch(batch_id: str, shipment_ids: list[str]) -> Batch`: Removes shipments from a batch.

### WarehouseService

The `WarehouseService` provides methods for interacting with warehouse-related endpoints in the ShipEngine API.

#### Methods

- `create_warehouse(warehouse_request: WarehouseRequest) -> Warehouse`: Creates a warehouse.
- `delete_warehouse(warehouse: Union[Warehouse, str]) -> None`: Deletes a warehouse.
- `get_by_id(warehouse_id: str) -> Warehouse`: Retrieves a warehouse by its ID.

### LabelService

The `LabelService` provides methods for interacting with label-related endpoints in the ShipEngine API.

#### Methods

- `purchase_label(label_request: LabelRequest) -> Label`: Purchases a shipping label.
- `create_return_label(label: Union[Label, str], return_label_request: ReturnLabelRequest) -> Label`: Creates a return label for an existing label.
- `get_by_id(label_id: str) -> Label`: Retrieves a label by its ID.
- `get_label_tracking_info(label: Union[Label, str]) -> TrackingInformation`: Retrieves tracking information for a label.

### TrackingService

The `TrackingService` provides methods for interacting with tracking-related endpoints in the ShipEngine API.

#### Methods

- `get_tracking_information(carrier_code: str, tracking_number: str) -> TrackingInformation`: Retrieves tracking information for a package.
- `start_tracking_package(carrier_code: str, tracking_number: str) -> None`: Starts tracking a package.
- `stop_tracking_package(carrier_code: str, tracking_number: str) -> None`: Stops tracking a package.

For detailed documentation on methods and parameters, refer to the source code or the [official ShipEngine API documentation](https://shipengine.github.io/shipengine-openapi/).