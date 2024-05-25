import json
from typing import Union

from attrs import asdict

from unofficial_shipengine.utils.serialize import serializer
from .models import Label, LabelRequest, ReturnLabelRequest
from ..common.services import BaseService
from ..shipments.models import Shipment
from ..tracking.models import TrackingInformation


class LabelService(BaseService):
    """
    LabelService provides methods for interacting with label-related endpoints in the ShipEngine API.

    Methods:
        purchase_label(label_request: LabelRequest) -> Label:
            Purchases a shipping label.

        create_return_label(label: Union[Label, str], return_label_request: ReturnLabelRequest) -> Label:
            Creates a return label for an existing label.

        get_by_id(label_id: str) -> Label:
            Retrieves a label by its ID.

        get_label_tracking_info(label: Union[Label, str]) -> TrackingInformation:
            Retrieves tracking information for a label.
    """

    def purchase_label(self, label_request: LabelRequest) -> Label:
        """
        Purchases a shipping label.

        Args:
            label_request (LabelRequest): The request data for purchasing a label.

        Returns:
            Label: The purchased Label object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = "https://api.shipengine.com/v1/labels"
        json_data = json.dumps(asdict(label_request, value_serializer=serializer))

        response = self.session.post(url, data=json_data)
        self._handle_response(response)
        response_dict = response.json()

        label: Label = Label.from_dict(response_dict)

        return label

    def create_return_label(
        self, label: Union[Label, str], return_label_request: ReturnLabelRequest
    ) -> Label:
        """
        Creates a return label for an existing label.

        Args:
            label (Union[Label, str]): The original label object or label ID.
            return_label_request (ReturnLabelRequest): The request data for creating a return label.

        Returns:
            Label: The created return Label object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        if isinstance(label, Label):
            label = label.label_id

        url = f"https://api.shipengine.com/v1/labels/{label}/return"
        json_data = json.dumps(
            asdict(return_label_request, value_serializer=serializer)
        )

        response = self.session.post(url, data=json_data)
        self._handle_response(response)
        response_dict = response.json()

        return_label: Label = Label.from_dict(response_dict)

        return return_label

    def get_by_id(self, label_id: str) -> Label:
        """
        Retrieves a label by its ID.

        Args:
            label_id (str): The ID of the label to retrieve.

        Returns:
            Label: The retrieved Label object.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        url = f"https://api.shipengine.com/v1/labels/{label_id}"
        response = self.session.get(url)
        self._handle_response(response)
        response_dict = response.json()

        label: Label = Label.from_dict(response_dict)

        return label

    def get_label_tracking_info(self, label: Union[Label, str]) -> TrackingInformation:
        """
        Retrieves tracking information for a label.

        Args:
            label (Union[Label, str]): The label object or label ID.

        Returns:
            TrackingInformation: The tracking information for the label.

        Raises:
            ShipEngineAPIError: If the response from the API is invalid.
        """
        if isinstance(label, Label):
            label = label.label_id

        url = f"https://api.shipengine.com/v1/labels/{label}/track"
        response = self.session.get(url)
        self._handle_response(response)
        response_dict = response.json()

        tracking_information: TrackingInformation = TrackingInformation.from_dict(
            response_dict
        )

        return tracking_information
