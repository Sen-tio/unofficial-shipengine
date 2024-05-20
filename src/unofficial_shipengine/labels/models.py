from enum import Enum

from attrs import define, field, validators

from ..common.models import Value, URL, Package
from ..shipments.models import ShipmentRequest
from .enums import ChargeEvent, LabelFormat, LabelLayout, DisplayScheme


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
class LabelRequest:
    shipment: ShipmentRequest
    # TODO: continue building
    charge_event: ChargeEvent = field(
        default=None, validator=validators.in_(ChargeEvent)
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
    charge_event: ChargeEvent = field(validator=validators.in_(ChargeEvent))
    service_code: str
    package: str
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
    label_image_id: str = field(default=None)
    batch_id: str = field(default=None)
    rma_number: str = field(default=None)

    @property
    def total_cost(self) -> Value:
        return Value(
            currency=self.shipment_cost.currency,
            amount=self.shipment_cost.amount + self.insurance_cost.amount,
        )
