from typing import Self, Any

from attrs import define, field


@define
class UnofficialShipEngineConfig:
    """
    UnofficialShipEngineConfig stores the configuration for the UnofficialShipEngine client.

    Attributes:
        api_key (str): The API key for authenticating with the ShipEngine API.
        retries (int): The number of retries for API requests in case of failure. Defaults to 3.
        backoff_factor (float): The backoff factor for retrying API requests. Defaults to 0.5.
    """

    api_key: str
    retries: int = field(default=3)
    backoff_factor: float = field(default=0.5)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
