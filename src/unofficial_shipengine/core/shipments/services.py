import json
from typing import Union, Optional

from attrs import asdict
from datetime import datetime

from unofficial_shipengine.utils.serialize import serializer
from .models import ShipmentRequest, Shipment
from ..common.services import BaseService
from ..common.enums import SortDir, SortBy


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

    def list_shipments(
        self,
        shipment_status: Optional[Union[Shipment.Status, str]] = None,
        batch_id: Optional[str] = None,
        tag: Optional[str] = None,
        created_at_start: Optional[Union[str, datetime]] = None,
        created_at_end: Optional[Union[str, datetime]] = None,
        modified_at_start: Optional[Union[str, datetime]] = None,
        modified_at_end: Optional[Union[str, datetime]] = None,
        page: int = 1,
        page_size: int = 25,
        sales_order_id: Optional[str] = None,
        sort_dir: Optional[Union[SortDir, str]] = SortDir.DESC,
        sort_by: Optional[Union[SortBy, str]] = None,
    ) -> list[Shipment]:
        filters = {
            "shipment_status": shipment_status,
            "batch_id": batch_id,
            "tag": tag,
            "created_at_start": (
                created_at_start.isoformat() if created_at_start else None
            ),
            "created_at_end": created_at_end.isoformat() if created_at_end else None,
            "modified_at_start": (
                modified_at_start.isoformat() if modified_at_start else None
            ),
            "modified_at_end": modified_at_end.isoformat() if modified_at_end else None,
            "page": page,
            "page_size": page_size,
            "sales_order_id": sales_order_id,
            "sort_dir": sort_dir,
            "sort_by": sort_by,
        }

        url = "https://api.shipengine.com/v1/shipments"
        params = {k: v for k, v in filters if v is not None}

        response = self.session.get(url, params=params)
        response_dict = response.json()

        self._handle_response(response)

        # TODO: this response also returns links to cycle through the pages, should probably return this as well

        return [Shipment.from_dict(s) for s in response_dict["shipments"]]
