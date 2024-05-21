import json
from typing import Union, Optional, Any

import requests
from attrs import asdict

from .models import Batch, BatchRequest, ProcessLabels
from ..core.exceptions import ShipEngineAPIError
from ..shipments.models import Shipment
from ..utils.serialize import serializer


class BatchService:

    def __init__(self, session: requests.Session):
        self.session = session

    def create_batch(self, batch_request: BatchRequest) -> Batch:
        data: str = json.dumps(asdict(batch_request, value_serializer=serializer))

        response = self.session.post("https://api.shipengine.com/v1/batches", data=data)
        response_dict = json.loads(response.text)

        if response.status_code in [400, 500]:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Batch.from_dict(response_dict)

    def get_by_id(self, batch_id: str) -> Batch:
        url: str = f"https://api.shipengine.com/v1/batches/{batch_id}"

        response = self.session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Batch.from_dict(response_dict)

    def process_labels(
        self, batch: Union[Batch, str], process_labels: ProcessLabels
    ) -> None:
        """Function can take a Batch object or a batch_id."""
        if isinstance(batch, Batch):
            batch = batch.batch_id

        data: str = json.dumps(asdict(process_labels, value_serializer=serializer))

        url: str = f"https://api.shipengine.com/v1/batches/{batch}/process/labels"

        response = self.session.post(url, data=data)

        if response.status_code != 204:
            response_dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

    def get_batch_errors(
        self, batch: Union[Batch, str], page: int = 1, pagesize: int = 1
    ) -> dict[str, Any]:
        if isinstance(batch, Batch):
            batch = batch.batch_id

        url: str = f"https://api.shipengine.com/v1/batches/{batch}/errors"
        response = self.session.get(
            url, params=json.dumps({"page": page, "pagesize": pagesize})
        )

        response_json: dict[str, Any] = response.json()

        return response_json

    def delete_batch(self, batch: Union[Batch, str]) -> None:
        if isinstance(batch, Batch):
            batch = batch.batch_id

        url: str = f"https://api.shipengine.com/v1/batches/{batch}"
        response = self.session.delete(url)

        if response.status_code != 204:
            response_dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

    def add_to_batch(
        self,
        batch: Union[Batch, str],
        shipments: list[Union[Shipment, str]],
        rates: Optional[list[str]] = None,
    ) -> None:
        self._modify_batch(batch, "add", shipments, rates)

    def remove_from_batch(
        self,
        batch: Union[Batch, str],
        shipments: list[Union[Shipment, str]],
        rates: Optional[list[str]] = None,
    ) -> None:
        self._modify_batch(batch, "remove", shipments, rates)

    def _modify_batch(
        self,
        batch: Union[Batch, str],
        endpoint: str,
        shipments: list[Union[str, Shipment]],
        rates: Optional[list[str]] = None,
    ) -> None:
        if isinstance(batch, Batch):
            batch = batch.batch_id

        shipments = [s if isinstance(s, str) else s.shipment_id for s in shipments]

        url: str = f"https://api.shipengine.com/v1/batches/{batch}/{endpoint}"
        data: str = json.dumps({"shipment_ids": shipments, "rate_ids": rates})
        response = self.session.post(url, data=data)

        if response.status_code != 204:
            response_dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )
