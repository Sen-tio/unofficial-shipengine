from attrs import define, field
from typing import Self, Any


@define
class UnofficialShipEngineConfig:
    api_key: str
    retries: int = field(default=3)
    backoff_factor: float = field(default=0.5)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
