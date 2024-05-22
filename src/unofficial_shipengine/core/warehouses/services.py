import json
from typing import Union

import requests
from attrs import asdict
from unofficial_shipengine.exceptions import ShipEngineAPIError
from unofficial_shipengine.utils.serialize import serializer

from .models import WarehouseRequest, Warehouse


class WarehouseService:

    def __init__(self, session: requests.Session):
        self.session = session

    def create_warehouse(self, warehouse_request: WarehouseRequest) -> Warehouse:
        data: str = json.dumps(asdict(warehouse_request, value_serializer=serializer))
        url = "https://api.shipengine.com/v1/warehouses"
        response = self.session.post(url, data=data)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Warehouse.from_dict(response_dict)

    def delete_warehouse(self, warehouse: Union[Warehouse, str]) -> None:
        if isinstance(warehouse, Warehouse):
            warehouse = warehouse.warehouse_id

        url = f"https://api.shipengine.com/v1/warehouses/{warehouse}"
        response = self.session.delete(url)

        if response.status_code != 204:
            response_dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

    def get_by_id(self, warehouse_id: str) -> Warehouse:
        url = f"https://api.shipengine.com/v1/warehouses/{warehouse_id}"
        response = self.session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        warehouse: Warehouse = Warehouse.from_dict(response_dict)

        return warehouse
