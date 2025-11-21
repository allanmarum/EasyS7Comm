"""Tests for the :mod:`easys7comm.plc` module.

The real snap7 client requires network access and a physical PLC.  To keep the
test suite self contained we mock the client interface.  This allows us to
verify the behaviour of the :class:`~easys7comm.plc.PLC` class without requiring
external resources.
"""

from unittest.mock import MagicMock, patch

from easys7comm import DataType, PLC
import snap7
from snap7 import util


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


def test_db_bool_read_and_write():
    """BOOL addresses include bit offsets when parsing values."""

    client = _mock_client()

    # Prepare DB read value with bit 3 set to True
    raw = bytearray(1)
    util.set_bool(raw, 0, 3, True)
    client.db_read.return_value = raw

    with patch("snap7.client.Client", return_value=client):
        plc = PLC("10.0.0.1")
        assert plc.read("DB1.DBX0.3", DataType.BOOL) is True
        plc.write("DB1.DBX0.3", False, DataType.BOOL)
        client.db_read.assert_called_once_with(1, 0, DataType.BOOL.size)
        client.db_write.assert_called_once()
        # Written value should have the requested bit cleared
        written_bytes = client.db_write.call_args.args[2]
        assert util.get_bool(written_bytes, 0, 3) is False
        plc.close()


def test_memory_area_read_and_write():
    """Non-DB addresses use the generic area read/write helpers."""

    client = _mock_client()
    # Reading from M10.0 should use area MK with provided bit
    raw = bytearray(1)
    util.set_bool(raw, 0, 0, True)
    client.read_area.return_value = raw

    with patch("snap7.client.Client", return_value=client):
        plc = PLC("10.0.0.1")
        assert plc.read("M10.0", DataType.BOOL) is True
        client.read_area.assert_called_once_with(snap7.type.Areas.MK, 0, 10, DataType.BOOL.size)

        plc.write("M10.0", False, DataType.BOOL)
        client.write_area.assert_called_once()
        area, db, offset, data = client.write_area.call_args.args
        assert area == snap7.type.Areas.MK
        assert db == 0
        assert offset == 10
        assert util.get_bool(data, 0, 0) is False
        plc.close()
