from typing import Any

import requests

from unofficial_shipengine.exceptions import ShipEngineAPIError


class BaseService:
    def __init__(self, session: requests.Session):
        self.session = session

    @staticmethod
    def _handle_response(response: requests.Response):
        if response.status_code in [200, 204, 207]:
            return

        response_dict: dict[str, Any] = response.json()

        raise ShipEngineAPIError(
            request_id=response_dict["request_id"], errors=response_dict["errors"]
        )
