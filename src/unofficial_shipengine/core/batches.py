import json
from enum import Enum
from attrs import define, field, validators, asdict
from .common import Error, URL, LabelDownload, serializer
from .exceptions import ShipEngineAPIError
from typing import Union, Self
from .. import session


class LabelLayout(Enum):
    FOUR_BY_SIX: str = "4x6"
    LETTER: str = "letter"


class LabelFormat(Enum):
    PDF: str = "pdf"
    PNG: str = "png"
    ZPL: str = "zpl"


@define
class ProcessLabels:

    class DisplayScheme(Enum):
        LABEL: str = "label"
        QR_CODE: str = "qr_code"
        LABEL_AND_QR_CODE: str = "label_and_qr_code"
        PAPERLESS: str = "paperless"
        LABEL_AND_PAPERLESS: str = "label_and_paperless"

    create_batch_and_process_labels: bool = field(default=True)
    ship_date: str = None

    label_layout: LabelLayout = field(
        default=LabelLayout.FOUR_BY_SIX, validator=validators.in_(LabelLayout)
    )

    label_format: LabelFormat = field(default=LabelFormat.PDF)

    display_scheme: DisplayScheme = field(
        default=DisplayScheme.LABEL, validator=validators.in_(DisplayScheme)
    )


@define
class BatchRequest:

    shipment_ids: list[str]
    rate_ids: list[str] = None
    external_batch_id: str = None
    batch_notes: str = None
    process_labels: ProcessLabels = None


@define
class Batch:
    class Status(Enum):
        OPEN: str = "open"
        QUEUED: str = "queued"
        PROCESSING: str = "processing"
        COMPLETED: str = "completed"
        COMPLETED_WITH_ERRORS: str = "completed_with_errors"
        ARCHIVED: str = "archived"
        NOTIFYING: str = "notifying"
        INVALID: str = "invalid"

    batch_id: str
    batch_number: str
    external_batch_id: str
    created_at: str
    processed_at: str
    errors: int
    process_errors: list[Error]
    warnings: int
    completed: int
    forms: int
    count: int
    batch_shipments_url: URL
    batch_labels_url: URL
    batch_errors_url: URL
    label_download: URL
    form_download: URL
    status: Status = field(validator=validators.in_(Status))
    paperless_download: URL = None
    batch_notes: str = None

    label_layout: Union[LabelLayout, None] = field(default=LabelLayout.FOUR_BY_SIX)
    label_format: LabelFormat = field(
        default=LabelFormat.PDF, validator=validators.in_(LabelFormat)
    )

    @classmethod
    def from_dict(cls, data: dict) -> "Batch":
        batch_shipments_url: URL = URL(**data.pop("batch_shipments_url"))
        batch_labels_url: URL = URL(**data.pop("batch_labels_url"))
        batch_errors_url: URL = URL(**data.pop("batch_errors_url"))
        label_download: LabelDownload = LabelDownload(**data.pop("label_download"))
        form_download: URL = URL(**data.pop("form_download"))

        return cls(
            batch_shipments_url=batch_shipments_url,
            batch_labels_url=batch_labels_url,
            batch_errors_url=batch_errors_url,
            label_download=label_download,
            form_download=form_download,
            **data,
        )

    @classmethod
    def create_batch(cls, batch_request: BatchRequest):
        data: str = json.dumps(asdict(batch_request, value_serializer=serializer))

        response = session.post("https://api.shipengine.com/v1/batches", data=data)
        response_dict = json.loads(response.text)

        if response.status_code in [400, 500]:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Batch.from_dict(response_dict)

    @classmethod
    def get_by_id(cls, batch_id: str) -> "Batch":
        url: str = f"https://api.shipengine.com/v1/batches/{batch_id}"

        response = session.get(url)
        response_dict: dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Batch.from_dict(response_dict)

    def process_labels(self, process_labels: ProcessLabels) -> None:
        data: str = json.dumps(asdict(process_labels, value_serializer=serializer))

        url: str = (
            f"https://api.shipengine.com/v1/batches/{self.batch_id}/process/labels"
        )

        response = session.post(url, data=data)

        if response.status_code != 204:
            response_dict: dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

    def get_batch_errors(self, page: int = 1, pagesize: int = 1) -> dict:
        url: str = f"https://api.shipengine.com/v1/batches/{self.batch_id}/errors"
        response = session.get(
            url, params=json.dumps({"page": page, "pagesize": pagesize})
        )

        return json.loads(response.text)

    def delete_batch(self) -> None:
        url: str = f"https://api.shipengine.com/v1/batches/{self.batch_id}"
        response = session.delete(url)

        if response.status_code != 204:
            response_dict: dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

    def add_to_batch(self, shipment_ids: list[str], rate_ids: list[str] = None) -> None:
        self._modify_batch("add", shipment_ids, rate_ids)

    def remove_from_batch(
        self, shipment_ids: list[str], rate_ids: list[str] = None
    ) -> None:
        self._modify_batch("remove", shipment_ids, rate_ids)

    def _modify_batch(
        self, endpoint: str, shipment_ids: list[str], rate_ids: list[str]
    ) -> None:
        url: str = f"https://api.shipengine.com/v1/batches/{self.batch_id}/{endpoint}"
        data: str = json.dumps({"shipment_ids": shipment_ids, "rate_ids": rate_ids})
        response = session.post(url, data=data)

        if response.status_code != 204:
            response_dict: dict = json.loads(response.text)
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )
