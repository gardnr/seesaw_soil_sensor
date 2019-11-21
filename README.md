# Adafruit STEMMA Soil Sensor - I2C Capacitive Moisture Sensor

Tested on Raspberry Pi 3 Model B V1.2

[Tutorial](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test)

On Raspi, make sure to [enable I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

```
python3 -m pip install -r seesaw_soil_sensor/requirements.txt

gardnr add metric soil moisture soil-moisture
gardnr add metric soil moisture soil-temp

gardnr add driver soil-sensor seesaw_soil_sensor.driver:SeesawSoilSensor
```
