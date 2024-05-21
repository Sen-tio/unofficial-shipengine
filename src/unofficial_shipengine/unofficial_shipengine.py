import requests

from .batches.services import BatchService
from .carriers.services import CarrierService
from .shipments.services import ShipmentService
from .warehouses.services import WarehouseService
from .labels.services import LabelService


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
