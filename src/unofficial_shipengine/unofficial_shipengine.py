from typing import Union

import requests
from requests.adapters import HTTPAdapter, Retry

from .core.batches.services import BatchService
from .core.carriers.services import CarrierService
from .core.labels.services import LabelService
from .core.shipments.services import ShipmentService
from .core.tracking.services import TrackingService
from .core.warehouses.services import WarehouseService
from .unofficial_shipengine_config import UnofficialShipEngineConfig


class UnofficialShipEngine:
    def __init__(
        self,
        config: Union[
            UnofficialShipEngineConfig, dict[str, Union[float, int, str]], str
        ],
    ) -> None:
        if isinstance(config, str):
            self.config = UnofficialShipEngineConfig(config)
        elif isinstance(config, dict):
            self.config = UnofficialShipEngineConfig.from_dict(config)
        elif isinstance(config, UnofficialShipEngineConfig):
            self.config = config

        self.session = self._create_session()

        self.shipments = ShipmentService(self.session)
        self.carriers = CarrierService(self.session)
        self.batches = BatchService(self.session)
        self.warehouses = WarehouseService(self.session)
        self.labels = LabelService(self.session)
        self.tracking = TrackingService(self.session)

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers = {
            "Host": "api.shipengine.com",
            "API-Key": self.config.api_key,
            "Content-Type": "application/json",
        }

        retry = Retry(
            total=self.config.retries,
            backoff_factor=self.config.backoff_factor,
            status_forcelist=[500, 502, 503, 504],
        )

        session.mount("https://", HTTPAdapter(max_retries=retry))

        return session
