
import time
import pycom
import pybytes
from CayenneLPP import CayenneLPP

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

# Disable heartbeat LED
pycom.heartbeat(False)

while True:
    pycom.rgbled(0x000014)
    lpp = CayenneLPP()

    print('\n\n** 3-Axis Accelerometer (LIS2HH12)')
    print('Acceleration', li.acceleration())
    print('Roll', li.roll())
    print('Pitch', li.pitch())
    lpp.add_accelerometer(1, li.acceleration()[0], li.acceleration()[1], li.acceleration()[2])
    lpp.add_gryrometer(1, li.roll(), li.pitch(), 0)

    print('\n\n** Digital Ambient Light Sensor (LTR-329ALS-01)')
    print('Light', lt.light())
    lpp.add_luminosity(1, lt.light()[0])
    lpp.add_luminosity(2, lt.light()[1])

    print('\n\n** Humidity and Temperature Sensor (SI7006A20)')
    print('Humidity', si.humidity())
    print('Temperature', si.temperature())
    lpp.add_relative_humidity(1, si.humidity())
    lpp.add_temperature(1, si.temperature())

    mpPress = MPL3115A2(py, mode=PRESSURE)
    print('\n\n** Barometric Pressure Sensor with Altimeter (MPL3115A2)')
    print('Pressure (hPa)', mpPress.pressure()/100)
    lpp.add_barometric_pressure(1, mpPress.pressure()/100)

    mpAlt = MPL3115A2(py, mode=ALTITUDE)
    print('Altitude', mpAlt.altitude())
    print('Temperature', mpAlt.temperature())
    lpp.add_gps(1, 0, 0, mpAlt.altitude())
    lpp.add_temperature(2, mpAlt.temperature())

    print('Sending data (uplink)...')
    pybytes.send_signal(1, lpp.get_buffer())
    pycom.rgbled(0x001400)
    time.sleep(30)
