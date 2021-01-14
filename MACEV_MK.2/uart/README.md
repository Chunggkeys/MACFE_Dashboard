# Raspberry Pi Testing Suit for UART
This folder contains the code base for testing UART communication using a Raspberry Pi.

- [UART](#uart)
- [GPS](#gps)
- [Testing](#testing)

## UART
To handle UART communication [pyserial](https://pyserial.readthedocs.io/en/latest/index.html) library is used and it is the only required external library to run the code. Install the library using the command below.

```
python3 -m pip install pyserial
```

### Preparing RPi to use GPIO UART port (on /dev/ttyAMA0)
By default, UART is using the inferior "mini UART" method on `/dev/ttyS0`. To change this behavior, we have to **disable** the onboard bluetooth that is occupying the "PL011" method on `/dev/ttyAMA0`. For more information please see the [official documentation](https://www.raspberrypi.org/documentation/configuration/uart.md).

#### Configuration
Following the steps below will turn on serial interface without a shell access and make sure that UART is working on PL011 mode on `/dev/ttyAMA0` by disabling bluetooth.

1. `sudo raspi-config` > Interface Options > Serial Port > No for shell access > Yes for serial port
2. In `/boot/config.txt`
    1. Append `enable_uart=1` (should be already added by raspi-config)
    2. Append `dtoverlay=disable_bt` (for more information: [link](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/arch/arm/boot/dts/overlays/disable-bt-overlay.dts))
    3. `sudo systemctl disable hciuart`
3. `sudo reboot`
4. `dmesg | grep serial` (should show which port the GPIO serial is initialized at)
    1. fe201000.serial: ttyAMA0 (<-- this should be ttyAMA0 not ttyS0)

#### Wiring
GPIO Header | Adaptor
:---------: | :------:
GND (6)     | GND
TX (8)      | RX
RX (10)     | TX

[Wiring Diagram](https://electropeak.com/learn/wp-content/uploads/2019/07/rpiard-1.jpg)

## GPS
The following modules are created with respect to [NMEA-0183](https://en.wikipedia.org/wiki/NMEA_0183) standard and the LS20030~3 [datasheet](https://cdn.sparkfun.com/datasheets/GPS/LS20030~3_datasheet_v1.3.pdf).

#### Processing Incoming Messages
A complete parsing class to digest GPS messages can be found in [parser.py](parser.py). The main `parse` method will parse any supported message and verify its checksum. If the message can be parsed and the checksum is correct, it will return a dictinary with all the values. The message must be supply in the form of `$CODE,...*CHECKSUM` like shown in the example.

```
data = Parser.parse('$GPGSA,A,3,17,28,30,01,13,24,15,11,06,,,,1.62,0.86,1.37*04')

data == {'mode1': 'A', 'mode2': '3', 'pdop': 1.62, 'vdop': 0.86, 'hdop': 1.37, 'checksum': '0x4', 'channel1': '17', 'channel2': '28', 'channel3': '30', 'channel4': '01', 'channel5': '13', 'channel6': '24', 'channel7': '15', 'channel8': '11', 'channel9': '06', 'channel10': '', 'channel11': '', 'channel12': ''}
```

#### Creating Test Messages
Constructing GPS messages by hand is a non-trivial job, that's why I created a struct for each GPS code in [structs.py](structs.py). Unfortunaetlly, I couldn't find a good way to create C like structs in Python so I used [dataclasses](https://docs.python.org/3/library/dataclasses.html) instead. Each GPS code has its own dataclass and they are created like initializing a regular class. You must supply an argument to each parameter while initializing, however, if a value is unknown or empty, you can simply pass `None`.

During initialization, a string will be created with a checksum for the message. To access the string, simply use the `string` variable like shown in the example.

```
gpgga = GPGGA(
    time='065938.200',
    latitude=4005.9932,
    latitude_dir='N',
    longitude=10509.9938,
    longitude_dir='W',
    fix_quality=1,
    satellites=9,
    hdop=0.86,
    altitude=1562.8,
    units='M',
    geoidal_separation=-20.7,
    age=None,
    station_id=None
)

gpgga.string == '$GPGGA,065938.200,4005.9932,N,10509.9938,W,1,9,0.86,1562.8,M,-20.7,M,,*5C'
```

#### Supported GPS Codes:
 - **GPGGA** - Global positioning system fixed data
 - **GPGLL** - Geographic position - latitude/longitude
 - **GPGSA** - GNSS DOP and active satellites
 - **GPGSV** - GNSS satellites in view
 - **GPRMC** - Recommended minimum specific GNSS data
 - **GPVTG** - Course over ground and ground speed
 
## Testing
[reader.py](reader.py) has a simple endless while loop that reads the serial port for incoming messages. If a message can be parsed, data will be printed on the terminal as key-value pairs.

[tester.py](tester.py) is a class made to automate sending messages over the serial port. In the `createStrings` method, all the messages must be created and appended to the `tests` array. Once the `test` method is called, each string in the `tests` array will be sent.

## Author
- Boran Seckin - <seckinb@mcmaster.ca>
