#!/usr/bin/python3

'''
parser.py
Author: Boran Seckin <seckinb@mcmaster.ca>
Last Modified: Jan. 06, 2021

This file contains the Parser class which is used to parse GPS messages formated
in NMEA-0183 standard into Python dictionaries. I have used the following datasheet
to format all the structs:

https://cdn.sparkfun.com/datasheets/GPS/LS20030~3_datasheet_v1.3.pdf

You can either use the specific parser method for each message or use the general
'parse' method to both parse any message and verify their checksums. Messages must
be supplied line by line.

Supported message ids:
    - GPGGA
    - GPGLL
    - GPGSA
    - GPGSV
    - GPRMC
    - GPVTG
'''

def try_int(string) -> int:
    try:
        return int(string)
    except ValueError:
        return string

def try_float(string) -> float:
    try:
        return float(string)
    except ValueError:
        return string

def try_hex(string) -> hex:
    try:
        return hex(int(string, 16))
    except ValueError:
        return string

class Parser:
    '''
    Parses NMEA-0183 formatted input.\n
    Reference: https://cdn.sparkfun.com/datasheets/GPS/LS20030~3_datasheet_v1.3.pdf
    '''

    @staticmethod
    def checksum(string) -> hex:
        '''
        Calculates the checksum for NMEA-0183 formatted input.\n
        Reference: https://en.wikipedia.org/wiki/NMEA_0183#C_implementation_of_checksum_generation
        '''
        string = string[1:].split('*')[0]
        c = 0
        for char in string:
            c ^= ord(char)
        return hex(c)

    @staticmethod
    def parse(input) -> dict:
        '''
        General method to parse any input. The input should be one line at a time
        and start with message id like '$CODE'. This function will also calculate
        and verify the checksum of the message.
        '''

        # Make sure the end of line char(s) are removed.
        if input.endswith('\r\n'):
            input = input[:-len('\r\n')]
        if input.endswith('\n'):
            input = input[:-len('\n')]

        # Verify the checksum
        try:
            if Parser.checksum(input) != try_hex(input.split('*')[1]):
                raise Exception('Checksum is incorrect!')
        except Exception as error:
            raise Exception('Cannot verify checksum!') from error

        if input[1:6] == 'GPGGA':
            return Parser.parseGPGGA(input)
        elif input[1:6] == 'GPGLL':
            return Parser.parseGPGLL(input)
        elif input[1:6] == 'GPGSA':
            return Parser.parseGPGSA(input)
        elif input[1:6] == 'GPGSV':
            return Parser.parseGPGSV(input)
        elif input[1:6] == 'GPRMC':
            return Parser.parseGPRMC(input)
        elif input[1:6] == 'GPVTG':
            return Parser.parseGPVTG(input)
        else:
            return None

    @staticmethod
    def parseTime(input):
        '''
        Returns a dict with parsed hour, minute and second values.\n
        Format: hhmmss.sss
        '''
        return {
            'hour': try_int(input[:2]),
            'min': try_int(input[2:4]),
            'sec': try_float(input[4:])
        }

    @staticmethod
    def parseGPGGA(input):
        data = input.split(',')
        return {
            'time': Parser.parseTime(data[1]),
            'latitude': try_float(data[2]),
            'latitude_dir': data[3],
            'longitude': try_float(data[4]),
            'longitude_dir': data[5],
            'fix_quality': try_int(data[6]),
            'satellites': try_int(data[7]),
            'hdop': try_float(data[8]),
            'altitude': try_float(data[9]),
            'units': data[10],
            'geoidal_separation': try_float(data[11]),
            'age': try_int(data[13]),
            'station_id': try_int(data[14].split('*')[0]),
            'checksum': try_hex(data[14].split('*')[1])
        }

    @staticmethod
    def parseGPGLL(input):
        data = input.split(',')
        return {
            'latitude': try_float(data[1]),
            'latitude_dir': data[2],
            'longitude': try_float(data[3]),
            'longitude_dir': data[4],
            'time': Parser.parseTime(data[5]),
            'status': data[6],
            'mode': data[7].split('*')[0],
            'checksum': try_hex(data[7].split('*')[1])
        }

    @staticmethod
    def parseGPGSA(input):
        data = input.split(',')
        output = {
            'mode1': data[1],
            'mode2': data[2],
            'pdop': try_float(data[-3]),
            'vdop': try_float(data[-2]),
            'hdop': try_float(data[-1].split('*')[0]),
            'checksum': try_hex(data[-1].split('*')[1])
        }

        # There are upto 12 channels from 1 to 12.
        for i in range(1, 13):
            output[f'channel{i}'] = data[i + 2]

        return output

    @staticmethod
    def parseGPGSV(input):
        data = input.split(',')
        output = {
            'total': try_int(data[1]),
            'current': try_int(data[2]),
            'satellites': try_int(data[3]),
            'checksum': try_hex(data[-1].split('*')[1])
        }
        data[-1] = data[-1].split('*')[0]   # remove the checksum for the next process

        '''
        GPGSV can have multiple messages to convey all the tracked satelites.
        Each message can transmit upto 4 satellites' information. The code below,
        parses the data according to the total number of messages (total), the current
        message's number (current) and the number of satellites (satellites).

        Only the last message might have less than 4 satellites.

        Note: Regardless the message number, channels on every message start from 1.
        '''
        remaining = output['satellites'] - ((output['current'] - 1) * 4)

        for i in range(1, min(remaining, 4) + 1):
            output[f'channel{i}'] = {
                'id': try_int(data[0 + (4 * i)]),
                'elevation': try_int(data[1 + (4 * i)]),
                'azimuth': try_int(data[2 + (4 * i)]),
                'snr': try_int(data[3 + (4 * i)]),
            }

        return output

    @staticmethod
    def parseGPRMC(input):
        data = input.split(',')
        return {
            'time': Parser.parseTime(data[1]),
            'status': data[2],
            'latitude': try_float(data[3]),
            'latitude_dir': data[4],
            'longitude': try_float(data[5]),
            'longitude_dir': data[6],
            'speed': try_float(data[7]),
            'course': try_float(data[8]),
            'date': {
                'raw': data[9],
                'day': try_int(data[9][:2]),
                'month': try_int(data[9][2:4]),
                'year': try_int(data[9][4:])
            },
            'magnetic_variation': data[10],
            'variation_sense': data[11],
            'mode': data[12].split('*')[0],
            'checksum': try_hex(data[12].split('*')[1])
        }

    @staticmethod
    def parseGPVTG(input):
        data = input.split(',')
        return {
            'course': {
                'true': try_float(data[1]),
                'magnetic': try_float(data[3])
            },
            'speed': {
                'knots': try_float(data[5]),
                'kph': try_float(data[7])
            },
            'mode': data[9].split('*')[0],
            'checksum': try_hex(data[9].split('*')[1])
        }
