import time

import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

from gardnr import drivers, metrics


class SeesawSoilSensor(drivers.Sensor):

    moisture_metric = 'soil-moisture'
    t9e_metric = 'soil-temp'

    def setup(self):
        i2c_bus = busio.I2C(SCL, SDA)
        self.ss = Seesaw(i2c_bus, addr=0x36)

    def read(self):
        # read moisture level through capacitive touch pad
        moisture = self.ss.moisture_read()
        metrics.create_metric_log(self.moisture_metric, moisture)

        # read temperature from the temperature sensor
        t9e = self.ss.get_temp()
        metrics.create_metric_log(self.t9e_metric, t9e)
