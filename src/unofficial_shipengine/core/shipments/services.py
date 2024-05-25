import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import ShipmentRequest, Shipment
from ..common.services import BaseService


class ShipmentService(BaseService):
    """
    ShipmentService provides methods for interacting with shipment-related endpoints in the ShipEngine API.

    Methods:
        create_shipment(shipment_request: Union[ShipmentRequest, list[ShipmentRequest]]) -> Union[Shipment, list[Shipment]]:
            Creates a shipment or a list of shipments.

        get_by_id(shipment_id: str) -> Shipment:
            Retrieves a shipment by its ID.

        get_by_external_id(external_shipment_id: str) -> Shipment:
            Retrieves a shipment by its external ID.

        update_shipment(shipment: Shipment) -> Shipment:
            Updates an existing shipment.

        cancel_shipment(shipment: Union[Shipment, str]) -> None:
            Cancels a shipment.
    """

    def create_shipment(
        self, shipment_request: Union[ShipmentRequest, list[ShipmentRequest]]
    ) -> Union[Shipment, list[Shipment]]:
        """
        Creates a shipment or a list of shipments.

        Args:
            shipment_request (Union[ShipmentRequest, list[ShipmentRequest]]): The shipment request or a list of shipment requests.

        Returns:
            Union[Shipment, list[Shipment]]: The created shipment or a list of created shipments.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        if isinstance(shipment_request, list):
            shipment_requests = shipment_request
        else:
            shipment_requests = [shipment_request]

        url = "https://api.shipengine.com/v1/shipments"
        data = [asdict(sr, value_serializer=serializer) for sr in shipment_requests]
        json_data: str = json.dumps({"shipments": data})

        response = self.session.post(url, data=json_data)
        self._handle_response(response)
        response_dict = response.json()

        shipments = [Shipment.from_dict(s) for s in response_dict["shipments"]]

        if isinstance(shipment_request, ShipmentRequest):
            return shipments[0]

        return shipments

    def get_by_id(self, shipment_id: str) -> Shipment:
        """
        Retrieves a shipment by its ID.

        Args:
            shipment_id (str): The ID of the shipment to retrieve.

        Returns:
            Shipment: The retrieved Shipment object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = f"https://api.shipengine.com/v1/shipments/{shipment_id}"

        response = self.session.get(url)
        self._handle_response(response)
        response_dict = response.json()

        return Shipment.from_dict(response_dict)

    def get_by_external_id(self, external_shipment_id: str) -> Shipment:
        """
        Retrieves a shipment by its external ID.

        Args:
            external_shipment_id (str): The external ID of the shipment to retrieve.

        Returns:
            Shipment: The retrieved Shipment object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = (
            f"https://api.shipengine.com/v1/shipments/"
            f"external_shipment_id/{external_shipment_id}"
        )

        response = self.session.get(url)
        self._handle_response(response)
        response_dict = response.json()

        return Shipment.from_dict(response_dict)

    def update_shipment(self, shipment: Shipment) -> Shipment:
        """
        Updates an existing shipment.

        Args:
            shipment (Shipment): The shipment object to update.

        Returns:
            Shipment: The updated Shipment object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = f"https://api.shipengine.com/v1/shipments/{shipment.shipment_id}"
        json_data = json.dumps(asdict(shipment, value_serializer=serializer))

        response = self.session.put(url, data=json_data)
        self._handle_response(response)
        response_dict = response.json()

        return Shipment.from_dict(response_dict)

    def cancel_shipment(self, shipment: Union[Shipment, str]) -> None:
        """
        Cancels a shipment.

        Args:
            shipment (Union[Shipment, str]): The shipment object or shipment ID to cancel.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        if isinstance(shipment, Shipment):
            shipment = shipment.shipment_id

        url = f"https://api.shipengine.com/v1/shipments/{shipment}/cancel"
        response = self.session.put(url)
        self._handle_response(response)
