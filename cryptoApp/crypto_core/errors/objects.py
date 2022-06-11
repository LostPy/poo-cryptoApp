from . import CryptoException


class ObjectException(CryptoException):
    """Base exception for exception related to objects data."""
    pass


class CurrencyError(ObjectException):
    """Exception raised for currencies related errors."""
    pass


class PortfolioError(ObjectException):
    """Exception raised for portfolios related errors."""
    pass


class TransactionError(ObjectException):
    """Exception raised for transactions related errors."""
    pass


class CurrencyNotFound(CurrencyError):
    """Exception raised when a currency was not found in database or API."""

    def __init__(self, currency_id: str):
        super().__init__(f"This currency was not found: '{currency_id}'")


class CurrencyDbNotFound(CurrencyNotFound):
    """Exception raised when a currency was not found in database."""
    pass


class CurrencyApiNotFound(CurrencyNotFound):
    """Exception raised when a currency was not found in API."""
    pass


class PortfolioAlreadyExists(PortfolioError):
    """Exception raised when a user created a portfolio already existing."""

    def __init__(self, portfolio_name: str):
        super().__init__(f"This portfolio already exists: '{portfolio_name}'")
