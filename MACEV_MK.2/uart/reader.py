#!/usr/bin/python3

'''
reader.py
Author: Boran Seckin <seckinb@mcmaster.ca>
Last Modified: Jan. 07, 2021

This file contains a usable CLI for the parser. When run, the code will
expect line by line input on serial port and try to parse each message.
'''

from uart import UART
from parser import Parser

uart = UART(timeout=None)

try:
    while True:
        msg = uart.readline()
        print(msg, end='')

        try:
            parsed = Parser.parse(msg)
            for pair in Parser.parse(msg).items():
                print('\t', f'{pair[0]}: {pair[1]}')
        except Exception:
            print('Unable to parse the message.')

        print()
except KeyboardInterrupt:
    pass
