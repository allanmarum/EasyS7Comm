# examples/basic_usage.py

from easys7comm import PLCInterface, DataType

def main():
    # Replace with your PLC's IP address and configuration
    plc = PLCInterface("127.0.0.1", 0, 1)
    
    try:
        # Example: read a STRING from DB7 at byte offset 6
        data = plc.read_db_row(7, 6, DataType.STRING)
        print("Read data:", data)
        
        # Example: write a REAL value to DB7 at byte offset 6
        plc.write_db_row(7, 6, 123.321, DataType.REAL)
        print("Write operation completed successfully.")
        
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        plc.disconnect()

if __name__ == "__main__":
    main()
