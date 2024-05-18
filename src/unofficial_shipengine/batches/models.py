from enum import Enum
from typing import Union

from attrs import define, field, validators

from src.unofficial_shipengine.common.models import URL, LabelDownload, Error
from .enums import LabelLayout, LabelFormat


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
