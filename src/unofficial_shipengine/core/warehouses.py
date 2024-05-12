import json
from typing import Self
from attrs import define, field, validators, asdict
from src.unofficial_shipengine.core.common import Address, serializer
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError
from .. import session


@define
class WarehouseRequest:
    name: str
    origin_address: Address
    return_address: Address = None
    is_default: bool = None


@define
class Warehouse:
    warehouse_id: str
    name: str
    created_at: str
    origin_address: Address
    return_address: Address
    is_default: bool = None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        origin_address: Address = Address(**data.pop("origin_address"))
        return_address: Address = Address(**data.pop("return_address"))
        return Warehouse(
            origin_address=origin_address, return_address=return_address, **data
        )

    @classmethod
    def create_warehouse(cls, warehouse_request: WarehouseRequest) -> Self:
        data: str = json.dumps(asdict(warehouse_request, value_serializer=serializer))
        url = "https://api.shipengine.com/v1/warehouses"
        response = session.post(url, data=data)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return cls.from_dict(response_dict)

    def delete_warehouse(self) -> None:
        url = f"https://api.shipengine.com/v1/warehouses/{self.warehouse_id}"
        response = session.delete(url)

        if response.status_code != 204:
            response_dict: dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )
