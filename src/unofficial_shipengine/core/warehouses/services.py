import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import WarehouseRequest, Warehouse
from ..common.services import BaseService


class WarehouseService(BaseService):

    def create_warehouse(self, warehouse_request: WarehouseRequest) -> Warehouse:
        data: str = json.dumps(asdict(warehouse_request, value_serializer=serializer))
        url = "https://api.shipengine.com/v1/warehouses"
        response = self.session.post(url, data=data)
        response_dict = json.loads(response.text)
        self._handle_response(response)

        return Warehouse.from_dict(response_dict)

    def delete_warehouse(self, warehouse: Union[Warehouse, str]) -> None:
        if isinstance(warehouse, Warehouse):
            warehouse = warehouse.warehouse_id

        url = f"https://api.shipengine.com/v1/warehouses/{warehouse}"
        response = self.session.delete(url)
        self._handle_response(response)

    def get_by_id(self, warehouse_id: str) -> Warehouse:
        url = f"https://api.shipengine.com/v1/warehouses/{warehouse_id}"
        response = self.session.get(url)
        response_dict = json.loads(response.text)
        self._handle_response(response)

        warehouse: Warehouse = Warehouse.from_dict(response_dict)

        return warehouse
