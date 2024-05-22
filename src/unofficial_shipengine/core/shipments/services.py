import json
from typing import Union

import requests
from attrs import asdict
from unofficial_shipengine.exceptions import ShipEngineAPIError
from unofficial_shipengine.utils.serialize import serializer

from .models import ShipmentRequest, Shipment


class ShipmentService:

    def __init__(self, session: requests.Session):
        self.session = session

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

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        shipments = [Shipment.from_dict(s) for s in response_dict["shipments"]]

        if isinstance(shipment_request, ShipmentRequest):
            return shipments[0]

        return shipments

    def get_by_id(self, shipment_id: str) -> Shipment:
        url = f"https://api.shipengine.com/v1/shipments/{shipment_id}"

        response = self.session.get(url)
        response_dict = response.json()

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Shipment.from_dict(response_dict)

    def get_by_external_id(self, external_shipment_id: str) -> Shipment:
        url = (
            f"https://api.shipengine.com/v1/shipments/"
            f"external_shipment_id/{external_shipment_id}"
        )

        response = self.session.get(url)
        response_dict = response.json()

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Shipment.from_dict(response_dict)

    def update_shipment(self, shipment: Shipment) -> Shipment:
        url = f"https://api.shipengine.com/v1/shipments/{shipment.shipment_id}"
        json_data = json.dumps(asdict(shipment, value_serializer=serializer))

        response = self.session.put(url, data=json_data)
        response_dict = response.json()

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Shipment.from_dict(response_dict)

    def cancel_shipment(self, shipment: Union[Shipment, str]) -> None:
        if isinstance(shipment, Shipment):
            shipment = shipment.shipment_id

        url = f"https://api.shipengine.com/v1/shipments/{shipment}/cancel"
        response = self.session.put(url)

        if response.status_code != 204:
            print(response.text)
            response_dict = response.json()
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )
