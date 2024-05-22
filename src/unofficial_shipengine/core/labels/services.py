import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import Label, LabelRequest, ReturnLabelRequest
from ..common.services import BaseService
from ..tracking.models import TrackingInformation


class LabelService(BaseService):

    def purchase_label(self, label_request: LabelRequest) -> Label:
        url = "https://api.shipengine.com/v1/labels"
        json_data = json.dumps(asdict(label_request, value_serializer=serializer))

        response = self.session.post(url, data=json_data)
        response_dict = response.json()

        self._handle_response(response)

        label: Label = Label.from_dict(response_dict)

        return label

    def create_return_label(
        self, label: Union[Label, str], return_label_request: ReturnLabelRequest
    ) -> Label:
        if isinstance(label, Label):
            label = label.label_id

        url = f"https://api.shipengine.com/v1/labels/{label}/return"
        json_data = json.dumps(
            asdict(return_label_request, value_serializer=serializer)
        )

        response = self.session.post(url, data=json_data)
        response_dict = response.json()

        self._handle_response(response)

        return_label: Label = Label.from_dict(response_dict)

        return return_label

    def get_by_id(self, label_id: str) -> Label:
        url = f"https://api.shipengine.com/v1/labels/{label_id}"
        response = self.session.get(url)
        response_dict = response.json()

        self._handle_response(response)

        label: Label = Label.from_dict(response_dict)

        return label

    def get_label_tracking_info(self, label: Union[Label, str]) -> TrackingInformation:
        if isinstance(label, Label):
            label = label.label_id

        url = f"https://api.shipengine.com/v1/labels/{label}/track"
        response = self.session.get(url)
        response_dict = response.json()

        self._handle_response(response)

        tracking_information: TrackingInformation = TrackingInformation.from_dict(
            response_dict
        )

        return tracking_information
