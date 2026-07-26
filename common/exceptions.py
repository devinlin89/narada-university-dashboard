class NaradaError(Exception):
    """Base exception for the Narada Dashboard."""


class ConfigurationError(NaradaError):
    """Raised when configuration is invalid or incomplete."""


class ValidationError(NaradaError):
    """Raised when input data fails validation."""