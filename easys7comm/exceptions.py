"""Custom exception hierarchy for EasyS7Comm."""


class S7Exception(Exception):
    """Base exception for all EasyS7Comm-related errors."""


class S7CommunicationError(S7Exception):
    """Raised when communication with the PLC fails."""


class S7AddressError(S7Exception):
    """Raised when an invalid PLC address is provided."""


class S7TimeoutError(S7CommunicationError):
    """Raised when a PLC operation exceeds the configured timeout."""
