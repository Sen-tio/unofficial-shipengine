import requests

from .shipments.services import ShipmentService
from .carriers.services import CarrierService
from .batches.services import BatchService


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
