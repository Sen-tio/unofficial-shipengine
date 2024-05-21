from typing import Any
from enum import Enum

from attrs import define, field, validators

from ..common.enums import ValidateAddress
from ..common.models import Value, URL, Package
from ..shipments.models import ShipmentRequest
from .enums import (
    ChargeEvent,
    LabelFormat,
    LabelLayout,
    DisplayScheme,
    LabelDownloadType,
)


@define
class LabelDownload:
    href: str
    pdf: str = field(default=None)
    zpl: str = field(default=None)
    png: str = field(default=None)


@define
class PaperlessDownload:
    href: str
    instructions: str = field(default=None)
    handoff_code: str = field(default=None)


@define
class ReturnLabelRequest:
    charge_event: ChargeEvent = field(
        default=ChargeEvent.CARRIER_DEFAULT, validator=validators.in_(ChargeEvent)
    )
    label_layout: LabelLayout = field(
        default=LabelLayout.FOUR_BY_SIX, validator=validators.in_(LabelLayout)
    )
    display_scheme: DisplayScheme = field(
        default=DisplayScheme.LABEL, validator=validators.in_(DisplayScheme)
    )
    label_format: LabelFormat = field(
        default=LabelFormat.PDF, validator=validators.in_(LabelFormat)
    )
    label_download_type: LabelDownloadType = field(
        default=LabelDownloadType.URL, validator=validators.in_(LabelDownloadType)
    )
    label_image_id: str = field(default=None)


@define
class LabelRequest:
    shipment: ShipmentRequest
    label_image_id: str = field(default=None)
    label_layout: LabelLayout = field(
        default=LabelLayout.FOUR_BY_SIX, validator=validators.in_(LabelLayout)
    )
    display_scheme: DisplayScheme = field(
        default=DisplayScheme.LABEL, validator=validators.in_(DisplayScheme)
    )
    label_format: LabelFormat = field(
        default=LabelFormat.PDF, validator=validators.in_(LabelFormat)
    )
    label_download_type: LabelDownloadType = field(
        default=LabelDownloadType.URL, validator=validators.in_(LabelDownloadType)
    )
    validate_address: ValidateAddress = field(
        default=ValidateAddress.NO_VALIDATION, validator=validators.in_(ValidateAddress)
    )
    outbound_label_id: str = field(default=None)
    charge_event: ChargeEvent = field(
        default=ChargeEvent.CARRIER_DEFAULT, validator=validators.in_(ChargeEvent)
    )
    is_return_label: bool = field(default=None)
    rma_number: str = field(default=None)
    ship_to_service_point_id: str = field(default=None)
    ship_form_service_point_id: str = field(default=None)


@define
class Label:
    @define
    class AlternativeIdentifier:
        type: str
        value: str

    class Status(Enum):
        PROCESSING: str = "processing"
        COMPLETED: str = "completed"
        ERROR: str = "error"
        VOIDED: str = "voided"

    class TrackingStatus(Enum):
        UNKNOWN: str = "unknown"
        IN_TRANSIT: str = "in_transit"
        ERROR: str = "error"
        DELIVERED: str = "delivered"

    label_id: str
    status: Status = field(validator=validators.in_(Status))
    shipment_id: str
    ship_date: str
    created_at: str
    shipment_cost: Value
    insurance_cost: Value
    requested_comparison_amount: Value
    tracking_number: str
    is_return_label: bool
    is_international: bool
    carrier_id: str
    charge_event: ChargeEvent
    service_code: str
    voided: bool
    voided_at: str
    trackable: bool
    carrier_code: str
    tracking_status: TrackingStatus = field(validator=validators.in_(TrackingStatus))
    label_download: LabelDownload
    form_download: URL
    paperless_download: PaperlessDownload
    insurance_claim: URL
    packages: list[Package]
    alternative_identifiers: list[AlternativeIdentifier] = field(default=None)
    label_format: LabelFormat = field(
        default=LabelFormat.PDF, validator=validators.in_(LabelFormat)
    )
    display_scheme: DisplayScheme = field(
        default=DisplayScheme.LABEL, validator=validators.in_(DisplayScheme)
    )
    label_layout: LabelLayout = field(
        default=LabelLayout.FOUR_BY_SIX, validator=validators.in_(LabelLayout)
    )
    rate_details: list[str] = field(default=None)
    label_image_id: str = field(default=None)
    batch_id: str = field(default=None)
    rma_number: str = field(default=None)
    package_code: str = field(default=None)
    qr_code_download: URL = field(default=None)
    shipping_rule_id: str = field(default=None)

    @property
    def total_cost(self) -> Value:
        return Value(
            currency=self.shipment_cost.currency,
            amount=self.shipment_cost.amount + self.insurance_cost.amount,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        if "form_download" in data.keys() and data["form_download"] is not None:
            form_download: URL = URL(**data.pop("form_download"))
        else:
            form_download = data.pop("form_download", None)

        if (
            "paperless_download" in data.keys()
            and data["paperless_download"] is not None
        ):
            paperless_download: PaperlessDownload = PaperlessDownload(
                **data.pop("paperless_download")
            )
        else:
            paperless_download = data.pop("paperless_download", None)

        label_download: LabelDownload = LabelDownload(**data.pop("label_download"))
        shipment_cost: Value = Value(**data.pop("shipment_cost"))
        insurance_cost: Value = Value(**data.pop("insurance_cost"))
        requested_comparison_amount: Value = Value(
            **data.pop("requested_comparison_amount")
        )

        packages = [Package.from_dict(p) for p in data.pop("packages")]

        return cls(
            label_download=label_download,
            form_download=form_download,
            shipment_cost=shipment_cost,
            insurance_cost=insurance_cost,
            requested_comparison_amount=requested_comparison_amount,
            paperless_download=paperless_download,
            packages=packages,
            **data
        )
