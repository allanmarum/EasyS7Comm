"""Tests for the :mod:`easys7comm.plc` module.

The real snap7 client requires network access and a physical PLC.  To keep the
test suite self contained we mock the client interface.  This allows us to
verify the behaviour of the :class:`~easys7comm.plc.PLC` class without requiring
external resources.
"""

from unittest.mock import MagicMock, patch

from easys7comm import PLC


def _mock_client(connected: bool = True) -> MagicMock:
    """Create a mocked snap7 client.

    Parameters
    ----------
    connected:
        Initial state returned by ``get_connected``.
    """

    mock = MagicMock()
    mock.connect.return_value = None
    mock.disconnect.return_value = None
    mock.destroy.return_value = None
    mock.get_connected.return_value = connected
    return mock


def test_plc_auto_connection():
    """The PLC connects on construction when ``auto_connect`` is left enabled."""
    with patch("snap7.client.Client", return_value=_mock_client(True)) as mock_cls:
        plc = PLC("10.0.0.1")
        assert plc.get_connected() is True
        plc.close()
        mock_cls.return_value.disconnect.assert_called_once()


def test_plc_manual_connection():
    """The PLC can defer connection until :meth:`PLC.connect` is called."""
    # First call to ``get_connected`` returns False; after ``connect`` it returns True.
    client = _mock_client(False)
    # First call before ``connect`` -> False, subsequent calls -> True
    client.get_connected.side_effect = [False, True, True]
    with patch("snap7.client.Client", return_value=client):
        plc = PLC("10.0.0.1", auto_connect=False)
        assert plc.get_connected() is False
        plc.connect()
        assert plc.get_connected() is True
        plc.close()
