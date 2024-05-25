import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import WarehouseRequest, Warehouse
from ..common.services import BaseService


class WarehouseService(BaseService):
    """
    WarehouseService provides methods for interacting with warehouse-related endpoints in the ShipEngine API.

    Methods:
        create_warehouse(warehouse_request: WarehouseRequest) -> Warehouse:
            Creates a warehouse.

        delete_warehouse(warehouse: Union[Warehouse, str]) -> None:
            Deletes a warehouse.

        get_by_id(warehouse_id: str) -> Warehouse:
            Retrieves a warehouse by its ID.
    """

    def create_warehouse(self, warehouse_request: WarehouseRequest) -> Warehouse:
        """
        Create a new warehouse.

        Args:
            warehouse_request (WarehouseRequest): An object representing the details of the warehouse to be created.

        Returns:
            Warehouse: An object representing the newly created warehouse.

        Raises:
            ShipEngineAPIError: If the request to create the warehouse fails.
        """
        data: str = json.dumps(asdict(warehouse_request, value_serializer=serializer))
        url = "https://api.shipengine.com/v1/warehouses"
        response = self.session.post(url, data=data)
        response_dict = json.loads(response.text)
        self._handle_response(response)

        return Warehouse.from_dict(response_dict)

    def delete_warehouse(self, warehouse: Union[Warehouse, str]) -> None:
        """
        Delete a warehouse.

        Args:
            warehouse (Union[Warehouse, str]): The warehouse object or ID of the warehouse to be deleted.

        Raises:
            ShipEngineAPIError: If the request to delete the warehouse fails.
        """
        if isinstance(warehouse, Warehouse):
            warehouse = warehouse.warehouse_id

        url = f"https://api.shipengine.com/v1/warehouses/{warehouse}"
        response = self.session.delete(url)
        self._handle_response(response)

    def get_by_id(self, warehouse_id: str) -> Warehouse:
        """
        Retrieve a warehouse by its ID.

        Args:
            warehouse_id (str): The ID of the warehouse to retrieve.

        Returns:
            Warehouse: An object representing the retrieved warehouse.

        Raises:
            ShipEngineAPIError: If the request to retrieve the warehouse fails.
        """
        url = f"https://api.shipengine.com/v1/warehouses/{warehouse_id}"
        response = self.session.get(url)
        response_dict = json.loads(response.text)
        self._handle_response(response)

        warehouse: Warehouse = Warehouse.from_dict(response_dict)

        return warehouse
