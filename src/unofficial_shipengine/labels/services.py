import json
import requests

from attrs import asdict

from ..core.exceptions import ShipEngineAPIError
from .models import Label, LabelRequest
from ..utils.serialize import serializer


class LabelService:
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def purchase_label(self, label_request: LabelRequest) -> Label:
        url = "https://api.shipengine.com/v1/labels"
        json_data = json.dumps(asdict(label_request, value_serializer=serializer))

        response = self.session.post(url, data=json_data)
        response_dict = response.json()

        if response.status_code != 200:
            raise ShipEngineAPIError(
                request_id=response_dict["request_id"], errors=response_dict["errors"]
            )

        label: Label = Label.from_dict(response_dict)

        return label
