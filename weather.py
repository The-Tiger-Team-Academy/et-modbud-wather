#!/usr/bin/env python3
from time import time, sleep
import minimalmodbus
import serial
from datetime import datetime as d
import pandas as pd
from influxdb_client import InfluxDBClient

instrument = minimalmodbus.Instrument('COM6', 247)
instrument.serial.port="COM6"                                       # this is the serial port name
instrument.serial.baudrate = 9600                                   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.5                                    # seconds
instrument.debug = False


# print("Date:",date.strftime("%Y-%m-%d"))
# print("Time:",date.strftime("%H:%M:%S"))
# print("Slave ID: ", instrument.read_register(registeraddress=0,signed=False,functioncode=4))
# print("SHT31 Temperature Adjust(Signed/10):",instrument.read_register(registeraddress=1,signed=True,functioncode=4))  
# print("SHT31 Humidity Adjust(Signed/10):", instrument.read_register(registeraddress=2,signed=True,functioncode=4))  
# print("FAN Interval Time(Minute):", instrument.read_register(registeraddress=3,signed=True,functioncode=4))  
# print("BH1750 Light Adjust(Signed/10):",instrument.read_register(registeraddress=4,signed=True,functioncode=4))  
# print("SHT31 Temperature Adjust(Float):", instrument.read_float(registeraddress=5,functioncode=4))  
# # print(instrument.read_float(registeraddress=6,functioncode=4))  
# print("SHT31 Humidity Adjust(Float):",instrument.read_float(registeraddress=7,functioncode=4))  
# # print(instrument.read_float(registeraddress=8,functioncode=4))  
# print("reserve:",instrument.read_float(registeraddress=9,functioncode=4))  
# # print(instrument.read_float(registeraddress=10,functioncode=4))  
# print("BH1750 Light Adjust(Float):",instrument.read_float(registeraddress=11,functioncode=4))  
# # print(instrument.read_float(registeraddress=12,functioncode=4))  
host="http://ip172-18-0-22-cceqdj0ja8q000ajl2rg-8086.direct.labs.play-with-docker.com"
token="4VTkB6sZNIFxDBX4T3XF89z1YCKEQsKSNbtsxQuz1tePDy9W9DIEH-K4W76pIi-NXT--9hzqhKI-kmiPVMDIOQ=="
port=8086
user="nitikornchumnankul"
password="123456789"
dbname="solar"
org="0f1ef4c15818986f"
# client = InfluxDBClient(host, port, user, password, dbname)
# client.create_database(dbname)
client = InfluxDBClient(url=host, token=token, org=org)

def read_data():
    date = d.now()
    data = {
        "date": date.strftime("%Y-%m-%d"),
        "time": date.strftime("%H:%M:%S"),
        "slave_id": instrument.read_register(registeraddress=0,signed=False,functioncode=4),
        "sht31_temperature_adjust_signed": instrument.read_register(registeraddress=1,signed=True,functioncode=4),
        "sht31_humidity_adjust_signed": instrument.read_register(registeraddress=2,signed=True,functioncode=4),
        "fan_interval_time_minute": instrument.read_register(registeraddress=3,signed=True,functioncode=4),
        "bh1750_light_adjust_signed":     instrument.read_register(registeraddress=4,signed=True,functioncode=4),
        "sht31_temperature_adjust_float": instrument.read_float(registeraddress=5,functioncode=4),
        "sht31_humidity_adjust_float":   instrument.read_float(registeraddress=7,functioncode=4),
        "reserve": instrument.read_float(registeraddress=9,functioncode=4),
        "bh1750_light_adjust_float": instrument.read_float(registeraddress=11,functioncode=4)
    }
    df = pd.DataFrame(data, columns = ["date", "time", "slave_id", "sht31_temperature_adjust_signed", "sht31_humidity_adjust_signed", "fan_interval_time_minute", "bh1750_light_adjust_signed", "sht31_temperature_adjust_float", "sht31_humidity_adjust_float", "reserve", "bh1750_light_adjust_float"], index=[0])
    return df

# def write_data(data):
#     # client.write_points(data)



count=0
day=1
convert_day_to_seconds = 60*60*24*day
store_data = pd.DataFrame()
while count !=10:
    count=count+1
    store_data = store_data.append(read_data())
   
    store_data.to_csv("weather.csv", index=False)
    sleep(0.8)
