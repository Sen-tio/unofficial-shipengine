import requests
import json

from typing import Union

from .models import Carrier, CarrierBalance
from src.unofficial_shipengine.core.exceptions import ShipEngineAPIError


class CarrierService:

    def __init__(self, session: requests.Session):
        self.session = session

    def get_carriers(self) -> list[Carrier]:
        url = "https://api.shipengine.com/v1/carriers"
        response = self.session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code not in [200, 207]:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        carriers = response_dict["carriers"]

        return [Carrier.from_dict(c) for c in carriers]

    def get_by_id(self, carrier_id: str) -> Carrier:
        url = f"https://api.shipengine.com/v1/carriers/{carrier_id}"
        response = self.session.get(url)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return Carrier.from_dict(response_dict)

    def add_funds(
        self, carrier: Union[Carrier, str], amount: float, currency: str = "usd"
    ) -> CarrierBalance:
        """
        There is no test mode for adding funds. You will be charged when you add funds.
        You can either pass a Carrier object or just the carrier_id as a string.
        """
        if isinstance(carrier, Carrier):
            carrier = carrier.carrier_id

        url = f"https://api.shipengine.com/v1/carriers/{carrier}/add_funds"
        data = {"amount": amount, "currency": currency}

        response = self.session.post(url, data=json.dumps(data))
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        return CarrierBalance.from_dict(response_dict)
