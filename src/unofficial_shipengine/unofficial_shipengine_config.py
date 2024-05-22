from attrs import define, field


@define
class UnofficialShipEngineConfig:
    api_key: str
    retries: int = field(default=3)
    backoff_factor: float = field(default=0.5)
