import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import ShipmentRequest, Shipment
from ..common.services import BaseService


class ShipmentService(BaseService):

    def create_shipment(
        self, shipment_request: Union[ShipmentRequest, list[ShipmentRequest]]
    ) -> Union[Shipment, list[Shipment]]:
        if isinstance(shipment_request, list):
            shipment_requests = shipment_request
        else:
            shipment_requests = [shipment_request]

        url = "https://api.shipengine.com/v1/shipments"
        data = [asdict(sr, value_serializer=serializer) for sr in shipment_requests]
        json_data: str = json.dumps({"shipments": data})

        response = self.session.post(url, data=json_data)
        response_dict = response.json()

        self._handle_response(response)

        shipments = [Shipment.from_dict(s) for s in response_dict["shipments"]]

        if isinstance(shipment_request, ShipmentRequest):
            return shipments[0]

        return shipments

    def get_by_id(self, shipment_id: str) -> Shipment:
        url = f"https://api.shipengine.com/v1/shipments/{shipment_id}"

        response = self.session.get(url)
        response_dict = response.json()
        self._handle_response(response)

        return Shipment.from_dict(response_dict)

    def get_by_external_id(self, external_shipment_id: str) -> Shipment:
        url = (
            f"https://api.shipengine.com/v1/shipments/"
            f"external_shipment_id/{external_shipment_id}"
        )

        response = self.session.get(url)
        response_dict = response.json()
        self._handle_response(response)

        return Shipment.from_dict(response_dict)

    def update_shipment(self, shipment: Shipment) -> Shipment:
        url = f"https://api.shipengine.com/v1/shipments/{shipment.shipment_id}"
        json_data = json.dumps(asdict(shipment, value_serializer=serializer))

        response = self.session.put(url, data=json_data)
        response_dict = response.json()
        self._handle_response(response)

        return Shipment.from_dict(response_dict)

    def cancel_shipment(self, shipment: Union[Shipment, str]) -> None:
        if isinstance(shipment, Shipment):
            shipment = shipment.shipment_id

        url = f"https://api.shipengine.com/v1/shipments/{shipment}/cancel"
        response = self.session.put(url)
        self._handle_response(response)
