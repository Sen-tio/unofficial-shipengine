import json
from typing import Self
from attrs import define, asdict

from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError

from .. import session


@define
class CarrierOption:
    name: str
    default_value: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)


@define
class CarrierPackage:
    package_id: str
    package_code: str
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)


@define
class CarrierService:
    carrier_id: str
    carrier_code: str
    service_code: str
    name: str
    domestic: bool
    international: bool
    is_multi_package_supported: bool

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)


@define
class Carrier:
    carrier_id: str
    carrier_code: str
    account_number: str
    requires_funded_amount: bool
    balance: float
    nickname: str
    friendly_name: str
    primary: bool
    has_multi_package_supporting_services: bool
    supports_label_messages: str
    disabled_by_billing_plan: bool
    funding_source_id: str
    packages: list[CarrierPackage] = []
    services: list[CarrierService] = []
    options: list[CarrierOption] = []

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        packages: list[CarrierPackage] = [
            CarrierPackage.from_dict(p) for p in data.pop("packages")
        ]

        services: list[CarrierService] = [
            CarrierService.from_dict(s) for s in data.pop("services")
        ]

        options: list[CarrierOption] = [
            CarrierOption.from_dict(o) for o in data.pop("options")
        ]

        return cls(packages=packages, services=services, options=options, **data)

    @classmethod
    def get_carriers(self) -> list[Self]:
        url = "https://api.shipengine.com/v1/carriers"
        response = session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code not in [200, 207]:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        carriers = response_dict["carriers"]

        return [self.from_dict(c) for c in carriers]

    @classmethod
    def get_by_id(cls, carrier_id: str) -> Self:
        url = f"https://api.shipengine.com/v1/carriers/{carrier_id}"
        response = session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return cls.from_dict(response_dict)
