import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('weather.csv',usecols= ["date", "time", "slave_id", "sht31_temperature_adjust_signed", "sht31_humidity_adjust_signed", "fan_interval_time_minute", "bh1750_light_adjust_signed", "sht31_temperature_adjust_float", "sht31_humidity_adjust_float", "reserve", "bh1750_light_adjust_float"])
df = pd.DataFrame(data)
print(df)

plt.plot(df["sht31_temperature_adjust_signed"])
plt.show()
