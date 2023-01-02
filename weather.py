#!/usr/bin/env python3
from time import time, sleep
import minimalmodbus
import serial
from datetime import datetime as d
import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


instrument = minimalmodbus.Instrument('COM3', 1)
instrument.serial.port="COM3"                                       # this is the serial port name
instrument.serial.baudrate = 2400                                   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.5                                    # seconds
instrument.debug = False


token = "jZP018mfywnVbNATa9YCu_oTwJ-4kZooMpZYAAqMJouTggcG6BoT6cC9W6nlLplYDPupwuOGi1FAOXFmlUAQ3Q=="
org = "eqtech"
bucket = "eqtech"

client = InfluxDBClient(url="http://192.168.1.123:8086", token=token)
write_voltage = client.write_api(write_options=SYNCHRONOUS)
write_watt = client.write_api(write_options=SYNCHRONOUS)
write_current = client.write_api(write_options=SYNCHRONOUS)
write_power_factor = client.write_api(write_options=SYNCHRONOUS)
write_frequency = client.write_api(write_options=SYNCHRONOUS)
write_export_active_energy= client.write_api(write_options=SYNCHRONOUS)
write_import_active_energy = client.write_api(write_options=SYNCHRONOUS)



def read_data():
    date = d.now()
    data = {
        "date": date.strftime("%Y-%m-%d"),
        "time": date.strftime("%H:%M:%S"),
        "slave_id": instrument.read_register(registeraddress=0, signed=False, functioncode=4),
        "Voltage": instrument.read_float(registeraddress=0, functioncode=4),
        "Watt": instrument.read_float(registeraddress=12, functioncode=4),
        "Current": instrument.read_float(registeraddress=6, functioncode=4),
        "Power factor": instrument.read_float(registeraddress=30, functioncode=4),
        "Frequency": instrument.read_float(registeraddress=70, functioncode=4),
        "Export active energy": instrument.read_float(registeraddress=74, functioncode=4),
        "Import active energy": instrument.read_float(registeraddress=72, functioncode=4),
    }
    df = pd.DataFrame(data, columns=["date", "time","slave_id", "Voltage", "Watt", "Current","Power factor", "Frequency", "Export active energy", "Import active energy"], index=[0])
    return df



count=0
day=2
convert_day_to_seconds = 60*60*24*day
store_data = pd.DataFrame()
while count !=convert_day_to_seconds:
     count=count+1
     data = read_data()
     voltage = {
          "measurement":"Voltage",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Voltage"][0],
          }
     }
     
     watt = {
          "measurement":"watt",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Watt"][0],
          }
     }
     current = {
          "measurement":"current",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Current"][0],
          }
     }
     power_factor = {
          "measurement":"power_factor",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value":  data["Power factor"][0],
          }
     }
     frequency = {
          "measurement":"frequency",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Frequency"][0],
          }
     }
     export_active_energy = {
          "measurement":"export_active_energy",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Export active energy"][0],
          }
     }
     import_active_energy = {
          "measurement":"import_active_energy",
          "tag":{
              "host":"host1"
          },
          "fields":{
              "value": data["Import active energy"][0],
          }
     }


    #  data = "mem,host=host1 used_percent=23.43234543"
    

     write_voltage.write(bucket, org, voltage)
     write_watt.write(bucket, org, watt)
     write_current.write(bucket, org, current)
     write_power_factor.write(bucket, org, power_factor)
     write_frequency.write(bucket, org, frequency)
     write_export_active_energy.write(bucket, org, export_active_energy)
     write_import_active_energy.write(bucket, org, import_active_energy)
     print(data["Import active energy"][0])


     #store_data = store_data.append(read_data())
    #  client.write_points(data)
     store_data.to_csv("weather1.csv", index=False)
     sleep(0.6)


# data = [
#     {
#         "measurement":"",
#         "tag":{
#           "location":"office"
#         },
#         "fields":{
#             "value"
#         }
#     }
# ]