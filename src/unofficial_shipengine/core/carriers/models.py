from typing import Self, Any

from attrs import define


@define
class CarrierOption:
    name: str
    default_value: str
    description: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@define
class CarrierPackage:
    package_id: str
    package_code: str
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
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
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@define
class CarrierBalance:
    currency: str
    amount: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
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
    def from_dict(cls, data: dict[str, Any]) -> Self:
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
