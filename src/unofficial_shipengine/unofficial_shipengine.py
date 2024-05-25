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
        """
        Initializes the UnofficialShipEngine client with the provided configuration.

        Args:
            config (Union[UnofficialShipEngineConfig, dict[str, Union[float, int, str]], str]):
                The configuration for the ShipEngine client. It can be an UnofficialShipEngineConfig object,
                a dictionary, or a string representing just the API key and the rest of the values will default.
        """
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
        """
        Parses the provided configuration into an UnofficialShipEngineConfig object.

        Args:
            config (Union[UnofficialShipEngineConfig, dict[str, Any], str]):
                The configuration to parse. It can be an UnofficialShipEngineConfig object,
                a dictionary, or a string representing just the API key and the rest of the values will default.

        Returns:
            UnofficialShipEngineConfig: The parsed configuration object.

        Raises:
            ValueError: If the configuration type is invalid.
        """
        if isinstance(config, str):
            return UnofficialShipEngineConfig(config)
        elif isinstance(config, Mapping):
            return UnofficialShipEngineConfig.from_dict(config)
        elif isinstance(config, UnofficialShipEngineConfig):
            return config
        else:
            raise ValueError("Invalid configuration type provided")

    def _create_session(self) -> requests.Session:
        """
        Creates a configured requests session for making API calls.

        Returns:
            requests.Session: The configured session with headers and retry strategy.
        """
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
