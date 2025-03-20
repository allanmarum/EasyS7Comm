# examples/basic_usage.py

"""
Basic Usage Example

This script demonstrates how to establish a connection with a PLC, 
read and write different types of data, and handle errors.

Usage:
    python basic_usage.py
"""

from easys7comm import PLC, DataType


def main():
    """
    Demonstrates basic PLC operations: writing and reading different data types.
    """
    plc_ip = "10.254.176.81"

    try:
        # Establish connection with the PLC
        plc = PLC(plc_ip)

        # Writing and reading different data types
        test_data = {
            "DB20.DBX12.0": ("Allan", DataType.STRING),  # String
            "DB20.DBD4": (42.5, DataType.REAL),  # Floating-point number
            "DB20.DBW8": (1234, DataType.INT),  # Integer (signed)
            "DB20.DBD10": (100000, DataType.DINT),  # Double integer
            "DB20.DBX14.0": (True, DataType.BOOL),  # Boolean value
            "DB20.DBD16": (3.1416, DataType.LREAL),  # Long real (double precision)
            "DB20.DBW20": (65535, DataType.UINT),  # Unsigned integer
            "DB20.DBD22": (1234567890, DataType.UDINT),  # Unsigned double integer
            "DB20.DBB26": (255, DataType.BYTE),  # Single byte value
            "DB20.DBW28": (0x1234, DataType.WORD),  # 16-bit word
            "DB20.DBD30": (0x12345678, DataType.DWORD),  # 32-bit double word
            "DB20.DBD34": (5000, DataType.TIME),  # Time value (milliseconds)
        }

        for address, (value, data_type) in test_data.items():
            print(f"Writing {value} to {address} as {data_type.name}")
            plc.write(address, value, data_type)
            read_value = plc.read(address, data_type)
            print(f"Read from {address}: {read_value} (Expected: {value})\n")

        # Check connection status
        print("PLC connected:", plc.get_connected())

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the PLC connection
        plc.close()


if __name__ == "__main__":
    main()
