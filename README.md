# EasyS7Comm

![In Development](https://img.shields.io/badge/status-In%20Development-yellow)

---

## ⚠️ Important Notice

**EasyS7Comm** is currently in the early stages of development and **is not ready for use in production**.

## Description

EasyS7Comm is a simplified abstraction of the powerful [Python-Snap7](https://github.com/gijzelaerr/python-snap7) tool. This project was created to make Snap7 **accessible to automation professionals with limited programming knowledge**. With EasyS7Comm, you can perform read and write operations on variables quickly and efficiently using minimal code.

While EasyS7Comm abstracts some of [Python-Snap7](https://github.com/gijzelaerr/python-snap7)'s advanced features, this trade-off is ideal for those who need straightforward and easy-to-use automation solutions.

## Features

- **Read Variables:** ![Read](https://img.shields.io/badge/read-partial-yellow)
- **Write Variables:** ![Write](https://img.shields.io/badge/write-not%20developed-red)
- **Simplified Connection:** ![Connection](https://img.shields.io/badge/read-partial-yellow)
- **Error Management:** ![Error Handling](https://img.shields.io/badge/error%20handling-not%20developed-red)

---
## Prerequisites

### Python
Ensure you have Python installed on your system.

### Snap7 DLL
- **Download**: You must download the `snap7.dll` from [SourceForge](https://sourceforge.net/projects/snap7/).
- **Configuration**: After downloading, place the `snap7.dll` in a directory that is accessible in your system's `PATH`. This ensures that EasyS7Comm can locate it during execution.

---
## Installation

Clone the repository and install the dependencies.

```Python
# Clone the repository
git clone https://github.com/your-username/easys7comm.git
cd easys7comm
```

> **Note:** If EasyS7Comm becomes available on PyPI in the future, installation might be as simple as using `pip install easys7comm`.

---
## How to Use

Below is an example demonstrating how to use EasyS7Comm for reading and writing operations with a PLC.

```Python
# examples/basic_usage.py
from easys7comm import PLC, DataType

def main():
    try:
        # Create a PLC instance with the specified IP address
        plc = PLC("192.168.0.2")
        
        # Write the string "Allan" to the PLC variable
        plc.write("DB20.DBX12.0", "Allan", DataType.STRING)
        
        # Read and print the value from the variable
        print(plc.read("DB20.DBX12.0", DataType.STRING))
        
        # Check and print if the connection is active
        print(plc.get_connected())
        
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        # Close the connection with the PLC
        plc.close()
```

> **Tip:** Ensure your PLC is properly configured and your network connection is stable to avoid connection issues.

