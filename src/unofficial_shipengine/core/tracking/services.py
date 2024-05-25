from unofficial_shipengine.core.tracking.models import TrackingInformation
from ..common.services import BaseService


class TrackingService(BaseService):
    """
    TrackingService provides methods for interacting with tracking-related endpoints in the ShipEngine API.

    Methods:
        get_tracking_information(carrier_code: str, tracking_number: str) -> TrackingInformation:
            Retrieves tracking information for a package.

        start_tracking_package(carrier_code: str, tracking_number: str) -> None:
            Starts tracking a package.

        stop_tracking_package(carrier_code: str, tracking_number: str) -> None:
            Stops tracking a package.
    """

    def get_tracking_information(
        self, carrier_code: str, tracking_number: str
    ) -> TrackingInformation:
        """
        Retrieves tracking information for a package.

        Args:
            carrier_code (str): The carrier code.
            tracking_number (str): The tracking number.

        Returns:
            TrackingInformation: The tracking information for the package.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = "https://api.shipengine.com/v1/tracking"
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}

        response = self.session.get(url, params=params)
        self._handle_response(response)
        response_dict = response.json()

        tracking_information: TrackingInformation = TrackingInformation.from_dict(
            response_dict
        )

        return tracking_information

    def start_tracking_package(self, carrier_code: str, tracking_number: str) -> None:
        """
        Starts tracking a package.

        Args:
            carrier_code (str): The carrier code.
            tracking_number (str): The tracking number.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        self._track_package("start", carrier_code, tracking_number)

    def stop_tracking_package(self, carrier_code: str, tracking_number: str) -> None:
        """
        Stops tracking a package.

        Args:
            carrier_code (str): The carrier code.
            tracking_number (str): The tracking number.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        self._track_package("stop", carrier_code, tracking_number)

    def _track_package(
        self, action: str, carrier_code: str, tracking_number: str
    ) -> None:
        """
        Internal method to start or stop tracking a package.

        Args:
            action (str): The action to perform ("start" or "stop").
            carrier_code (str): The carrier code.
            tracking_number (str): The tracking number.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = f"https://api.shipengine.com/v1/tracking/{action}"
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}
        response = self.session.post(url, params=params)
        self._handle_response(response)
