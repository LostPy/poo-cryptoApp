from . import CryptoException


class ApiException(CryptoException):
    """Base exception for API errors."""
    pass


class ApiConnectionError(ApiException):
    """Exception raised when the connection to API failed."""

    def __init__(self):
        super().__init__("Can't get a connection to the host: 'api.coingecko.com', "
                         "please, check your internet connection.")


class ApiRequestsError(ApiException):
    """Base exception for requests error (bad parameters...)"""
    pass


class ApiCurrencyNotFound(ApiRequestsError):
    """Exceptions raised when a bad currency id is passed in parameters."""

    def __init__(self, crypto_id: str):
        super().__init__(f"The currency '{crypto_id}' does not exist in API.")

