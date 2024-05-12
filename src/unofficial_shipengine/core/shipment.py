import json
from enum import Enum
from typing import Self

from attrs import define, field, validators, asdict

from src.unofficial_shipengine.core.common import (
    Address,
    AddressValidation,
    Package,
    Weight,
    serializer,
)
from .exceptions import ShipEngineAPIError
from .. import session


@define
class ShipmentRequest:
    class ValidateAddress(Enum):
        NO_VALIDATION: str = "no_validation"
        VALIDATE_ONLY: str = "validate_only"
        VALIDATE_AND_CLEAN: str = "validate_and_clean"

    class Confirmation(Enum):
        NONE: str = "none"
        DELIVERY: str = "delivery"
        SIGNATURE: str = "signature"
        ADULT_SIGNATURE: str = "adult_signature"
        DIRECT_SIGNATURE: str = "direct_signature"
        DELIVERY_MAILED: str = "delivery_mailed"
        VERBAL_CONFIRMATION: str = "verbal_confirmation"

    class InsuranceProvider(Enum):
        NONE: str = "none"
        SHIPSURANCE: str = "shipsurance"
        CARRIER: str = "carrier"
        THIRD_PARTY: str = "third_party"

    carrier_id: str
    service_code: str
    ship_to: Address
    packages: list[Package]
    ship_from: Address = None
    external_order_id: str = None
    external_shipment_id: str = None
    shipment_number: str = None
    tax_identifiers: list = None
    ship_date: str = None
    warehouse_id: str = None
    is_return: Address = None
    items: list = None
    customs: object = None
    order_source_code: str = None
    comparison_rate_type: str = None

    validate_address: ValidateAddress = field(
        default=ValidateAddress.VALIDATE_ONLY,
        validator=validators.in_(ValidateAddress),
    )

    confirmation: Confirmation = field(
        default=Confirmation.NONE, validator=validators.in_(Confirmation)
    )

    insurance_provider: InsuranceProvider = field(
        default=InsuranceProvider.NONE, validator=validators.in_(InsuranceProvider)
    )


@define(kw_only=True)
class Shipment(ShipmentRequest):
    errors: list[str]
    shipment_id: str
    modified_at: str
    created_at: str
    shipment_status: str
    return_to: Address  # TODO should be in Request
    advanced_options: list[str]  # TODO should be in Request
    shipping_rule_id: str
    tags: list[str]  # Todo should be in request
    total_weight: Weight

    # These fields can appear on shipment creation
    errors: list[str] = None
    address_validation: AddressValidation = None

    @classmethod
    def from_dict(cls, data: dict) -> "Shipment":
        # todo recursive on nested objects
        ship_to = Address(**data.pop("ship_to"))
        ship_from = Address(**data.pop("ship_from"))
        return_to = Address(**data.pop("return_to"))
        total_weight = Weight(**data.pop("total_weight"))

        return cls(
            ship_to=ship_to,
            ship_from=ship_from,
            return_to=return_to,
            total_weight=total_weight,
            **data,
        )

    @classmethod
    def create_shipment(cls, shipment_request: ShipmentRequest) -> Self:
        assert isinstance(shipment_request, ShipmentRequest)

        data_dict: dict = asdict(shipment_request, value_serializer=serializer)
        data: str = json.dumps({"shipments": [data_dict]})

        response = session.post("https://api.shipengine.com/v1/shipments", data=data)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return cls.from_dict(response_dict["shipments"][0])

    @classmethod
    def get_by_id(cls, shipment_id: str) -> "Shipment":
        response = session.get(f"https://api.shipengine.com/v1/shipments/{shipment_id}")
        response_dict = json.loads(response.text)

        return cls.from_dict(response_dict)

    def cancel(self) -> None:  # TODO add to this
        url: str = f"https://api.shipengine.com/v1/shipments/{self.shipment_id}/cancel"

        response = session.put(url)

        if response.status_code != 204:
            response_dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )


def create_multiple_shipments(shipments: list[ShipmentRequest]) -> list[Shipment]:
    data: str = json.dumps([asdict(s, value_serializer=serializer) for s in shipments])

    url: str = "https://api.shipengine.com/v1/shipments"
    response = session.post(url, data=data)
    response_dict = json.loads(response.text)

    if response.status_code != 200:
        raise ShipEngineAPIError(
            request_id=response_dict["request_id"], errors=response_dict["errors"]
        )

    shipments: list[Shipment] = [Shipment.from_dict(s) for s in shipments]

    return shipments
