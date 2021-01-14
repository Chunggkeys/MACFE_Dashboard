#!/usr/bin/python3

'''
structs.py
Author: Boran Seckin <seckinb@mcmaster.ca>
Last Modified: Jan. 06, 2021

This file has data classes (closest thing to C type structs that I could find) to
create GPS messages formated in NMEA-0183 standard. I have used the following datasheet
to format all the structs.

https://cdn.sparkfun.com/datasheets/GPS/LS20030~3_datasheet_v1.3.pdf

To create a message, simply use classes to create the string. If a field is unknown,
initialize it with the value 'None'. Upon initializing, each class will generate the formatted
string in the 'string' variable.
'''

from dataclasses import dataclass

def calcChecksum(string) -> hex:
    '''
    Calculates the checksum for NMEA-0183 formatted input.\n
    Reference: https://en.wikipedia.org/wiki/NMEA_0183#C_implementation_of_checksum_generation
    '''
    string = string[1:]
    c = 0
    for char in string:
        c ^= ord(char)
    return hex(c)

def addChecksum(string, checksum) -> str:
    '''
    Adds the hex representation of the checksum to the end of the
    string with a star and without '0x'.
    '''
    # Used 'upper' to make sure letters in hex is uppercase
    checksum = checksum.split('x')[1].upper()

    if len(f'{checksum}') < 2:
        return f'{string}*0{checksum}'
    
    return f'{string}*{checksum}'

def printNumber(number: int, length: int) -> str:
    '''
    Returns the string representation of number with
    the correct length by adding zero(s) to the beginning.
    '''
    string = str(number)
    while len(string) < length:
        string = f'0{string}'

    return string

def checkNone(value):
    '''
    If a value is none, simply returns empty string.
    '''
    if value != None:
        return value
    return ''

## Structs

@dataclass
class GPGGA:
    string: str
    code: str
    checksum: hex
    time: str
    latitude: float
    latitude_dir: 'N' or 'S'
    longitude: float
    longitude_dir: 'W' or 'E'
    fix_quality: int
    satellites: int
    hdop: float
    altitude: float
    units1: 'M' or 'I'
    geoidal_separation: float
    units2: 'M' or 'I'
    age: int
    station_id: int
    
    def __init__(
        self,
        time: str,
        latitude: float,
        latitude_dir: 'N' or 'S',
        longitude: float,
        longitude_dir: 'W' or 'E',
        fix_quality: int,
        satellites: int,
        hdop: float,
        altitude: float,
        units: 'M' or 'I',
        geoidal_separation: float,
        age: int,
        station_id: int
    ):
        self.code = 'GPGGA'
        self.time = time
        self.latitude = latitude
        self.latitude_dir = latitude_dir
        self.longitude = longitude
        self.longitude_dir = longitude_dir
        self.fix_quality = fix_quality
        self.satellites = satellites
        self.hdop = hdop
        self.altitude = altitude
        self.units1 = units
        self.geoidal_separation = geoidal_separation
        self.units2 = units
        self.age = age
        self.station_id = station_id

        self.string = self.stringify()                          # This will create a temporary string without the checksum.
        self.checksum = calcChecksum(self.string)               # The cheksum will be calculated with the temporary string.

        self.string = addChecksum(self.string, self.checksum)   # This will add the checksum and finialize the string.

    def stringify(self) -> str:
        '''
        Returns the concatenated string of each variable in the class.
        This will iterate over the variables in the order which they were initialized.
        '''
        string = '$'
        for key in vars(self):
            attr = getattr(self, key)
            string += f'{checkNone(attr)},'

        return string[:-1]  # Removes the last comma after the concat

@dataclass
class GPGLL:
    string: str
    code: str
    checksum: hex
    latitude: float
    latitude_dir: 'N' or 'S'
    longitude: float
    longitude_dir: 'W' or 'E'
    time: str
    status: str
    mode: str

    def __init__(
        self,
        latitude: float,
        latitude_dir: 'N' or 'S',
        longitude: float,
        longitude_dir: 'W' or 'E',
        time: str,
        status: str,
        mode: str,
    ):
        self.code = 'GPGLL'
        self.latitude = latitude
        self.latitude_dir = latitude_dir
        self.longitude = longitude
        self.longitude_dir = longitude_dir
        self.time = time
        self.status = status
        self.mode = mode

        self.string = self.stringify()
        self.checksum = calcChecksum(self.string)

        self.string = addChecksum(self.string, self.checksum)

    def stringify(self) -> str:
        string = '$'
        for key in vars(self):
            attr = getattr(self, key)
            string += f'{checkNone(attr)},'

        return string[:-1]

@dataclass
class GPGSVChannel:
    '''
    This class is meant to be used by the actual GPGSV class.
    '''
    id: int
    elevation: int
    azimuth: int
    snr: int

    def __init__(self, id: int, elevation: int, azimuth: int, snr: int):
        self.id = id
        self.elevation = elevation
        self.azimuth = azimuth
        self.snr = snr

    def stringify(self):
        string = ''
        for key in vars(self):
            attr = getattr(self, key)

            # Unlike other values, azimuth must have 3
            if key == 'azimuth':
                string += f'{printNumber(checkNone(attr), 3)},'
            else:
                string += f'{printNumber(checkNone(attr), 2)},'

        return string[:-1]

@dataclass
class GPGSV:
    string: str
    code: str
    checksum: hex
    total: int
    current: int
    satellites: int
    channels: [GPGSVChannel]

    def __init__(
        self,
        total: int,
        current: int,
        satellites: int,
        channels: [GPGSVChannel]
    ):
        self.code = 'GPGSV'
        self.total = total
        self.current = current
        self.satellites = satellites
        self.channels = channels

        self.string = self.stringify()
        self.checksum = calcChecksum(self.string)

        self.string = addChecksum(self.string, self.checksum)

    def stringify(self) -> str:
        string = f'${self.code},{self.total},{self.current},{self.satellites}'
        for channel in self.channels:
            string = f'{string},{channel.stringify()}'
        return string

@dataclass
class GPGSA:
    string: str
    code: str
    checksum: hex
    mode1: str
    mode2: str
    channels: [int]
    pdop: float
    vdop: float
    hdop: float

    def __init__(self, mode1: str, mode2: str, channels: [int], pdop: float, vdop: float, hdop: float):
        self.code = 'GPGSA'
        self.mode1 = mode1
        self.mode2 = mode2
        self.channels = channels
        self.pdop = pdop
        self.vdop = vdop
        self.hdop = hdop

        self.string = self.stringify()
        self.checksum = calcChecksum(self.string)

        self.string = addChecksum(self.string, self.checksum)

    def stringify(self) -> str:
        string = f'${self.code},{checkNone(self.mode1)},{checkNone(self.mode2)}'

        for i in range(12):
            if i < len(self.channels):
                # Channel ids must be 2 char long
                string = f'{string},{printNumber(self.channels[i], 2)}'
            else:
                string = f'{string},'

        string = f'{string},{checkNone(self.pdop)},{checkNone(self.vdop)},{checkNone(self.hdop)}'

        return string

@dataclass
class GPRMC:
    string: str
    code: str
    checksum: hex
    time: str
    status: str
    latitude: float
    latitude_dir: 'N' or 'S'
    longitude: float
    longitude_dir: 'W' or 'E'
    speed: float
    course: float
    date: str
    magnetic_variation: float
    variation_sense: 'E' or 'W'
    mode: str

    def __init__(
        self,
        time: str,
        status: str,
        latitude: float,
        latitude_dir: 'N' or 'S',
        longitude: float,
        longitude_dir: 'W' or 'E',
        speed: float,
        course: float,
        day: int,
        month: int,
        year: int,
        magnetic_variation: float,
        variation_sense: 'E' or 'W',
        mode: str
    ):
        self.code = 'GPRMC'
        self.time = time
        self.status = status
        self.latitude = latitude
        self.latitude_dir = latitude_dir
        self.longitude = longitude
        self.longitude_dir = longitude_dir
        self.speed = speed
        self.course = course
        self.date = f'{printNumber(day, 2)}{printNumber(month, 2)}{printNumber(year, 2)}'
        self.magnetic_variation = magnetic_variation
        self.variation_sense = variation_sense
        self.mode = mode

        self.string = self.stringify()
        self.checksum = calcChecksum(self.string)

        self.string = addChecksum(self.string, self.checksum)

    def stringify(self):
        string = '$'
        for key in vars(self):
            attr = getattr(self, key)
            string += f'{checkNone(attr)},'

        return string[:-1]

@dataclass
class GPVTG:
    string: str
    code: str
    checksum: hex
    course_true: float
    course_magnetic: float
    speed_knots: float
    speed_kph: float
    mode: str

    def __init__(
        self,
        course_true: float,
        course_magnetic: float,
        speed_knots: float,
        speed_kph: float,
        mode: str
    ):
        self.code = 'GPVTG'
        self.course_true = course_true
        self.course_magnetic = course_magnetic
        self.speed_knots = speed_knots
        self.speed_kph = speed_kph
        self.mode = mode
        
        self.string = self.stringify()
        self.checksum = calcChecksum(self.string)

        self.string = addChecksum(self.string, self.checksum)

    def stringify(self):
        '''
        This function is not good as others because I had to hard code units.
        '''
        return f'${checkNone(self.code)},{checkNone(self.course_true)},T,{checkNone(self.course_magnetic)},M,{checkNone(self.speed_knots)},N,{checkNone(self.speed_kph)},K,{checkNone(self.mode)}'

## Examples
'''
#$GPGGA,065938.200,4005.9932,N,10509.9938,W,1,9,0.86,1562.8,M,-20.7,M,,*5C
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

#$GPGSA,A,3,17,28,30,01,13,24,15,11,06,,,,1.62,0.86,1.37*04
gpgsa = GPGSA(
    mode1='A',
    mode2=3,
    channels=[17,28,30,1,13,24,15,11,6],
    pdop=1.62,
    vdop=0.86,
    hdop=1.37
)

#$GPGLL,4005.9932,N,10509.9938,W,065938.200,A,A*4E
gpgll = GPGLL(
    latitude=4005.9932,
    latitude_dir='N',
    longitude=10509.9938,
    longitude_dir='W',
    time='065938.200',
    status='A',
    mode='A'
)

#$GPGSV,4,1,13,17,80,265,43,28,62,054,36,19,48,235,,30,41,156,33*78
gpgsv = GPGSV(
    total=4,
    current=1,
    satellites=13,
    channels=[
        GPGSVChannel(id=17, elevation=80, azimuth=265, snr=43),
        GPGSVChannel(id=28, elevation=62, azimuth=54, snr=36),
        GPGSVChannel(id=19, elevation=48, azimuth=235, snr=None),
        GPGSVChannel(id=30, elevation=41, azimuth=156, snr=33)
    ]
)

#$GPRMC,065938.200,A,4005.9932,N,10509.9938,W,0.01,57.88,261118,,,A*47
gprmc = GPRMC(
    time='065938.200',
    status='A',
    latitude=4005.9932,
    latitude_dir='N',
    longitude=10509.9938,
    longitude_dir='W',
    speed=0.01,
    course=57.88,
    day=26,
    month=11,
    year=18,
    magnetic_variation='',
    variation_sense='',
    mode='A'
)

#$GPVTG,57.88,T,,M,0.01,N,0.01,K,A*0F
gpvtg = GPVTG(
    course_true=57.88,
    course_magnetic=None,
    speed_knots=0.01,
    speed_kph=0.01,
    mode='A'
)
'''
