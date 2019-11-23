import busio
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA

from gardnr import drivers, metrics


class SeesawSoilSensor(drivers.Sensor):

    i2c_address = 56  # 0x36
    moisture_metric = 'soil-moisture'
    t9e_metric = 'soil-temp'

    def setup(self):
        i2c_bus = busio.I2C(SCL, SDA)
        self.ss = Seesaw(i2c_bus, addr=self.ic2_address)

    def read(self):
        # read moisture level through capacitive touch pad
        moisture = self.ss.moisture_read()
        metrics.create_metric_log(self.moisture_metric, moisture)

        # read temperature from the temperature sensor
        t9e = self.ss.get_temp()
        metrics.create_metric_log(self.t9e_metric, t9e)
