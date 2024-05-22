import requests

from .core.batches.services import BatchService
from .core.carriers.services import CarrierService
from .core.shipments.services import ShipmentService
from .core.warehouses.services import WarehouseService
from .core.labels.services import LabelService


class UnofficialShipEngine:
    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.headers = {
            "Host": "api.shipengine.com",
            "API-Key": api_key,
            "Content-Type": "application/json",
        }

        self.shipments = ShipmentService(self.session)
        self.carriers = CarrierService(self.session)
        self.batches = BatchService(self.session)
        self.warehouses = WarehouseService(self.session)
        self.labels = LabelService(self.session)

        # TODO: setup retry strategy
        #   create proper fixtures for tests
