#!/usr/bin/python3

'''
tester.py
Author: Boran Seckin <seckinb@mcmaster.ca>
Last Modified: Jan. 07, 2021

This file contains the tester class that creates and sends GPS messages
over serial port. Using the structs create a desired message in 'createStrings'
method and append the string to tests variable.
'''

import structs
from uart import UART

class Tester:
    uart: UART
    tests: [str] = []

    def __init__(self):
        self.uart = UART(timeout=None)
        self.createStrings()

    def createStrings(self):
        gpgga = structs.GPGGA(
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

        self.tests.append(gpgga.string)

        gpgsa = structs.GPGSA(
            mode1='A',
            mode2=3,
            channels=[17,28,30,1,13,24,15,11,6],
            pdop=1.62,
            vdop=0.86,
            hdop=1.37
        )

        self.tests.append(gpgsa.string)

    def test(self):
        for string in self.tests:
            self.uart.write(string)

tester = Tester()
tester.test()
