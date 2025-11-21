"""Helper utilities for EasyS7Comm."""

from __future__ import annotations

from snap7.client import Client


def ensure_connected(client: Client) -> None:
    """Validate that the provided Snap7 client is connected.

    Args:
        client: The Snap7 client instance to validate.

    Raises:
        ConnectionError: If the client is not connected to any PLC.
    """

    if not client.get_connected():
        raise ConnectionError("Client is not connected to a PLC. Call connect() first.")
