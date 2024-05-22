from typing import Union, Mapping, Any

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
        self.config = self._parse_config(config)
        self._session = self._create_session()

        self.shipments = ShipmentService(self._session)
        self.carriers = CarrierService(self._session)
        self.batches = BatchService(self._session)
        self.warehouses = WarehouseService(self._session)
        self.labels = LabelService(self._session)
        self.tracking = TrackingService(self._session)

    @staticmethod
    def _parse_config(
        config: Union[UnofficialShipEngineConfig, dict[str, Any], str],
    ) -> UnofficialShipEngineConfig:
        if isinstance(config, str):
            return UnofficialShipEngineConfig(config)
        elif isinstance(config, Mapping):
            return UnofficialShipEngineConfig.from_dict(config)
        elif isinstance(config, UnofficialShipEngineConfig):
            return config
        else:
            raise ValueError("Invalid configuration type provided")

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

    # TODO: create list_<service> for the remaining services, use some sort of
    #   filter object/typed dictionary for filter params

    # TODO: finishing touches, type hinting, clean up UnofficialShipEngine class

    # TODO: write documentation and comments on complex code

    # TODO: write tests for any remaining uncovered code
