from typing import Self

from attrs import define

from src.unofficial_shipengine.common.models import Address


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
