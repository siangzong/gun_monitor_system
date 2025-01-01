#!/usr/bin/env python
import os
import sys
import serial
import threading
import time
from arduino_return import *
from scan import *

COM_PORT_1 = 'COM3'
COM_PORT_2 = 'COM4'
BAUD_RATES = 9600
"""啟動串列執行緒"""
def start_serial_threads():
    """啟動串列執行緒"""
    try:
        ser = serial.Serial(COM_PORT_1,BAUD_RATES)
        ser2 = serial.Serial(COM_PORT_2, BAUD_RATES)

        # 啟動背景執行緒
        serial_thread = threading.Thread(target=read_key, args=(ser,))
        serial_thread.daemon = True
        serial_thread.start()

        rfid_thread = threading.Thread(target=read_rfid, args=(ser2,))
        rfid_thread.daemon = True
        rfid_thread.start()

        qr_thread = threading.Thread(target=scan_qr)
        qr_thread.daemon = True
        qr_thread.start()

        return [ser, ser2]

    except serial.SerialException as e:
        print(f"無法打開串列埠：{e}")
        return []

    except Exception as e:
        print(f"發生錯誤：{e}")
        return []

def cleanup(serial_ports):
    """清理資源"""
    for ser in serial_ports:
        if ser and ser.is_open:
            ser.close()
    print("資源清理完成。")

if __name__ == "__main__":
    try:
        # 啟動執行緒並返回串列埠資源
        serial_ports = start_serial_threads()

        # 主執行緒保持運行，避免程式直接退出
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n程式中斷，正在清理資源...")
        cleanup(serial_ports)

    except Exception as e:
        print(f"程式發生未預期的錯誤：{e}")
        cleanup(serial_ports)