class ShipEngineAPIError(Exception):
    """Base class for all ShipEngine API errors."""

    def __init__(self, request_id: str, errors: list):
        self.request_id = request_id
        self.errors = errors
        super().__init__(self._format_message())

    def _format_message(self):
        return f"ShipEngine API Error (Request ID: {self.request_id}): {self.errors}"
