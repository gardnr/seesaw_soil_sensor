# Python 2.6 required.
if (sys.version_info < (2, 6)):
    python_version = ".".join(map(str, sys.version_info[:3]))
    print('Python version 2.6 or higher required, you are using \
        {}'.format(python_version))
    sys.exit()

# Prints usage information.
def print_usage():
    print('Usage:\n')
    print('{} <address> [[set] [new address]]\n'.format(sys.argv[0]))
    print('Examples:\n')
    print('Run continous measurements.')
    print('{} 0x20\n'.format(sys.argv[0]))
    print('Change the I2C address of the sensor on address 0x20 to 0x21')
    print('{} 0x20 set 0x21'.format(sys.argv[0]))
    print(len(sys.argv))
    sys.exit()

# Check command line argument for I2C address. (In hex, ie 0x20)
if (len(sys.argv) == 1) or (len(sys.argv) >= 5):
    print_usage()
if len(sys.argv) >= 2:
    if sys.argv[1].startswith("0x"):
        addr = int(sys.argv[1], 16)
    else:
        print_usage()

# Variables for calibrated max and min values. These need to be adjusted!
# These are only needed if you plan to use moist_percent.
# If these values are not adjusted for your sensor the value for
# moist_percent might go below 0% and above 100%
min_moist = 240
max_moist = 750

highest_measurement = False
lowest_measurement = False

# Initialize the sensor.
chirp = Chirp(address=addr,
              read_moist=True,
              read_temp=True,
              read_light=True,
              min_moist=min_moist,
              max_moist=max_moist,
              temp_scale='celsius',
              temp_offset=0)

# Check command line arguments if user wants to change the I2C address.
if len(sys.argv) >= 3:
    if sys.argv[2] == 'set':

        if sys.argv[3].startswith("0x"):
            new_addr = int(sys.argv[3], 16)
        else:
            new_addr = int(sys.argv[3])
        # Set new address, also resets the sensor.
        chirp.sensor_address = new_addr
        print('Chirp I2C address changed to {}'.format(hex(new_addr)))
        sys.exit()
    else:
        print_usage()

# Check which temperature sign to use.
if chirp.temp_scale == 'celsius':
    scale_sign = '°C'
elif chirp.temp_scale == 'farenheit':
    scale_sign = '°F'
elif chirp.temp_scale == 'kelvin':
    scale_sign = 'K'

print('Chirp soil moisture sensor.\n')
print('Firmware version:   {}'.format(hex(chirp.version)))
print('I2C address:        {}\n'.format(chirp.sensor_address))
print('Press Ctrl-C to exit.\n')
print('Moisture  | Temp   | Brightness')
print('-' * 31)

try:
    # Endless loop, taking measurements.
    while True:
        # Trigger the sensors and take measurements.
        chirp.trigger()
        output = '{:d} {:4.1f}% | {:3.1f}{} | {:d}'
        output = output.format(chirp.moist, chirp.moist_percent,
                               chirp.temp, scale_sign, chirp.light)
        print(output)
        # Adjust max and min measurement variables, used for calibrating
        # the sensor and allow using moisture percentage.
        if highest_measurement is not False:
            if chirp.moist > highest_measurement:
                highest_measurement = chirp.moist
        else:
            highest_measurement = chirp.moist
        if lowest_measurement is not False:
            if chirp.moist < lowest_measurement:
                lowest_measurement = chirp.moist
        else:
            lowest_measurement = chirp.moist
        time.sleep(1)
except KeyboardInterrupt:
    print('\nCtrl-C Pressed! Exiting.\n')
finally:
    print('Lowest moisture measured:  {}'.format(lowest_measurement))
    print('Highest moisture measured: {}'.format(highest_measurement))
    print('Bye!')
