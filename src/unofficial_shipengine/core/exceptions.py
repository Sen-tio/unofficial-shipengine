class ShipEngineAPIError(Exception):
    def __init__(self, request_id, errors):
        self.request_id = request_id
        self.errors = errors

    def __str__(self):
        error_messages = "\n".join(
            [
                f"Error Source: {error['error_source']}, Error Type: {error['error_type']}, "
                f"Error Code: {error['error_code']}, Message: {error['message']}"
                for error in self.errors
            ]
        )
        return f"ShipEngine API Error. Request ID: {self.request_id}\nErrors:\n{error_messages}"
