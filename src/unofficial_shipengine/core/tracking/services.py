import requests
from unofficial_shipengine.exceptions import ShipEngineAPIError

from unofficial_shipengine.core.tracking.models import TrackingInformation


class TrackingService:
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def get_tracking_information(
        self, carrier_code: str, tracking_number: str
    ) -> TrackingInformation:
        url = "https://api.shipengine.com/v1/tracking"
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}

        response = self.session.get(url, params=params)
        response_dict = response.json()

        if response.status_code != 200:
            response_dict = response.json()
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        tracking_information: TrackingInformation = TrackingInformation.from_dict(
            response_dict
        )

        return tracking_information

    def start_tracking_package(self, carrier_code: str, tracking_number: str) -> None:
        self._track_package("start", carrier_code, tracking_number)

    def stop_tracking_package(self, carrier_code: str, tracking_number: str) -> None:
        self._track_package("stop", carrier_code, tracking_number)

    def _track_package(
        self, action: str, carrier_code: str, tracking_number: str
    ) -> None:
        url = f"https://api.shipengine.com/v1/tracking/{action}"
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}

        response = self.session.post(url, params=params)

        if response.status_code != 204:
            response_dict = response.json()
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )
