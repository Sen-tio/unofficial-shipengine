from typing import Any, Self

from attrs import define

from .enums import TrackingStatusCode


@define
class TrackEvent:
    occurred_at: str
    carrier_occurred_at: str
    description: str
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    company_name: str
    signer: str
    event_code: str
    carrier_detail_code: str
    status_code: TrackingStatusCode
    status_description: str
    carrier_status_code: str
    carrier_status_description: str
    latitude: float
    longitude: float


@define
class TrackingInformation:

    tracking_number: str
    tracking_url: str
    status_code: TrackingStatusCode
    carrier_code: str
    carrier_id: str
    status_description: str
    carrier_status_code: str
    carrier_detail_code: str
    carrier_status_description: str
    ship_date: str
    estimated_delivery_date: str
    actual_delivery_date: str
    exception_description: str
    events: list[TrackEvent]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        events: list[TrackEvent] = [TrackEvent(**e) for e in data.pop("events")]
        return cls(events=events, **data)
