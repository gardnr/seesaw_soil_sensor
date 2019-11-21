import time
 
import busio 
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

from gardnr import drivers, metrics


class SeesawSoilSensor(drivers.Sensor):

    def setup(self):
        i2c_bus = busio.I2C(SCL, SDA)
        self.ss = Seesaw(i2c_bus, addr=0x36)

    def read(self):
        # read moisture level through capacitive touch pad
        touch = ss.moisture_read()
 
        # read temperature from the temperature sensor
        temp = ss.get_temp()


