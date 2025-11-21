# EasyS7Comm

![In Development](https://img.shields.io/badge/status-In%20Development-yellow)

---

## ⚠️ Important Notice

**EasyS7Comm** is currently in the early stages of development and **is not ready for use in production**.

## Description

EasyS7Comm is a compact abstraction layer over [Python-Snap7](https://github.com/gijzelaerr/python-snap7) designed to help automation professionals interact with Siemens PLCs using a few lines of Python. It streamlines connection handling and provides high-level helpers for reading and writing common data types.

While the project is still young, it already supports core PLC interactions without needing to touch raw Snap7 buffers.

## Features

- **Read Variables:** ![Read](https://img.shields.io/badge/read-implemented-green) Read DB, memory (M), input (I), and output (Q) areas, including bit-level access for booleans.
- **Write Variables:** ![Write](https://img.shields.io/badge/write-implemented-green) Write to DB, M, I, and Q addresses with type validation and bit-aware BOOL writes.
- **Simplified Connection:** ![Connection](https://img.shields.io/badge/connection-implemented-green) Automatically connect on initialization or defer with `auto_connect=False`.
- **Error Management:** ![Error Handling](https://img.shields.io/badge/error%20handling-basic-blue) Converts Snap7 errors into clear Python exceptions for connection failures and unsupported operations.

---
## Prerequisites

### Python
Ensure you have Python installed on your system.

### Snap7 DLL
- **Download**: You must download the `snap7.dll` from [SourceForge](https://sourceforge.net/projects/snap7/).
- **Configuration**: After downloading, place the `snap7.dll` in a directory that is accessible in your system's `PATH`. This ensures that EasyS7Comm can locate it during execution.

> On Linux you will typically need the Snap7 shared library (e.g., `libsnap7.so`). Refer to the Snap7 project instructions for your platform.

---
## Installation

Clone the repository and install the dependencies.

```Python
# Clone the repository
git clone https://github.com/your-username/easys7comm.git
cd easys7comm
pip install -r requirements.txt
```

> **Note:** If EasyS7Comm becomes available on PyPI in the future, installation might be as simple as using `pip install easys7comm`.

---
## How to Use

### Quick Example

```Python
# examples/basic_usage.py
from easys7comm import PLC, DataType

def main():
    plc = PLC("192.168.0.2")  # pass auto_connect=False to delay connection

    # Write a value to a DB address (bit-level BOOL supported)
    plc.write("DB20.DBX12.0", True, DataType.BOOL)

    # Read back the value
    value = plc.read("DB20.DBX12.0", DataType.BOOL)
    print("DB20.DBX12.0:", value)

    # Read from memory, input, or output areas
    print("M0.0:", plc.read("M0.0", DataType.BOOL))
    print("I4:", plc.read("I4", DataType.BYTE))
    print("Q8:", plc.read("Q8", DataType.BYTE))

    plc.close()

if __name__ == "__main__":
    main()
```

> **Tip:** Ensure your PLC is properly configured and your network connection is stable to avoid connection issues.

### Supported Address Formats

- **DB**: `DB{number}.{type}{byte}[.{bit}]` (e.g., `DB1.DBD0`, `DB20.DBX12.0`). Bit is required for `DBX` (BOOL) and must be omitted for other types.
- **Memory (M)**: `M{byte}[.{bit}]` (e.g., `M0`, `M10.2`).
- **Inputs (I)**: `I{byte}[.{bit}]` (e.g., `I0`, `I4.1`).
- **Outputs (Q)**: `Q{byte}[.{bit}]` (e.g., `Q0`, `Q8.7`).

### Data Types

Pass one of the `DataType` enum members to control parsing and serialization. Common options include:

- `DataType.BOOL` (bit-aware)
- `DataType.BYTE`, `DataType.WORD`, `DataType.DWORD`
- `DataType.INT`, `DataType.DINT`, `DataType.REAL`, `DataType.LREAL`
- `DataType.STRING` / `DataType.FS_STRING`

> Some types are read-only or write-only depending on Snap7 support. The library raises a `ValueError` if a write is attempted on a read-only type.

