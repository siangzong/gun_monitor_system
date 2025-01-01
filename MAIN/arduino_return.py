import serial
import time
import threading
from Lineapp.func import *
from auto_sent import *




def read_key(ser):
    while True:
        if ser.in_waiting > 0: 
            mcu_feedback = ser.readline().decode().strip()  
            ans = arduino_check_pass(mcu_feedback)
            if ans == 1:
                state = arduino_update_cabinet(mcu_feedback)
                rows = alert_open(mcu_feedback)
                print(state)
                if state == 'close':
                    ser.write(b'turn_on\n')  
                    time.sleep(0.5)
                elif state == 'open':
                    ser.write(b'turn_off\n')  
                    time.sleep(0.5)
                alert(rows)
            elif ans == 0:
                ser.write(b'not pass\n')
                time.sleep(0.5)

            print(mcu_feedback)

def read_rfid(ser):
    while True:
        if ser.in_waiting > 0: 
            global feedback 
            feedback= ser.readline().decode().strip()  
            arduino_update_rfid(feedback)
def process_data():
    if feedback:
        return feedback

def read_sql(ser):
    while True:
        if ser.in_waiting > 0: 
            mcu_feedback = ser.readline().decode().strip()  
            return(mcu_feedback)





