import json
from typing import Union

from .models import Carrier, CarrierBalance
from ..common.services import BaseService


class CarrierService(BaseService):
    """
    CarrierService provides methods for interacting with carrier-related endpoints in the ShipEngine API.

    Methods:
        get_carriers() -> list[Carrier]:
            Retrieves a list of carriers.

        get_by_id(carrier_id: str) -> Carrier:
            Retrieves a carrier by its ID.

        add_funds(carrier: Union[Carrier, str], amount: float, currency: str = "usd") -> CarrierBalance:
            Adds funds to a carrier account.
    """

    def get_carriers(self) -> list[Carrier]:
        """
        Retrieves a list of carriers.

        Returns:
            list[Carrier]: A list of Carrier objects.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = "https://api.shipengine.com/v1/carriers"
        response = self.session.get(url)
        response_dict = json.loads(response.text)

        self._handle_response(response)

        carriers = response_dict["carriers"]

        return [Carrier.from_dict(c) for c in carriers]

    def get_by_id(self, carrier_id: str) -> Carrier:
        """
        Retrieves a carrier by its ID.

        Args:
            carrier_id (str): The ID of the carrier to retrieve.

        Returns:
            Carrier: The retrieved Carrier object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = f"https://api.shipengine.com/v1/carriers/{carrier_id}"
        response = self.session.get(url)
        response_dict = json.loads(response.text)

        self._handle_response(response)

        return Carrier.from_dict(response_dict)

    def add_funds(
        self, carrier: Union[Carrier, str], amount: float, currency: str = "usd"
    ) -> CarrierBalance:
        """
        Adds funds to a carrier account.

        Note: There is no test mode for adding funds. You will be charged when you add funds.
              You can either pass a Carrier object or just the carrier_id as a string.

        Args:
            carrier (Union[Carrier, str]): The carrier object or carrier ID to add funds to.
            amount (float): The amount of funds to add.
            currency (str, optional): The currency in which to add funds. Defaults to "usd".

        Returns:
            CarrierBalance: The updated CarrierBalance object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        if isinstance(carrier, Carrier):
            carrier = carrier.carrier_id

        url = f"https://api.shipengine.com/v1/carriers/{carrier}/add_funds"
        data = {"amount": amount, "currency": currency}

        response = self.session.post(url, data=json.dumps(data))
        response_dict = json.loads(response.text)

        self._handle_response(response)

        return CarrierBalance.from_dict(response_dict)
