#!/usr/bin/python3

'''
uart.py
Author: Boran Seckin <seckinb@mcmaster.ca>
Last Modified: Jan. 10, 2021

This file is a simple wrapper of the Python library 'pyserial'.
https://pyserial.readthedocs.io/en/latest/index.html
'''

import sys
import time
import serial

class UART:
    ser: serial.Serial = None

    PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
    STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
    FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

    def __init__(
        self,
        port: str = '/dev/serial0',    # Default for RPi
        baudrate: int = 57600,
        bytesize: (FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS) = EIGHTBITS,
        parity: (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE) = PARITY_NONE,
        stopbits: (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO) = STOPBITS_ONE,
        timeout: float or None = 0.5
    ):
        try:
            self.ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
        except serial.SerialException as error:
            sys.exit(error)

        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

        print(f'UART is initialized at {port} - {baudrate} - {bytesize} - {parity} - {stopbits} - {timeout}')

    def write(self, input, end='\n', encoding='utf-8') -> int:
        '''
        Writes the input (concatted with the end variable, if encoding) to serial port as bytes encoded
        as utf-8 by defualt. If instead you want to send the raw message in bytes, set the encoding to None.\n
        Returns the number of bytes written.
        '''
        if not encoding:
            written = self.ser.write(input)
        else:
            written = self.ser.write(f'{input}{end}'.encode(encoding))

        # Write is not blocking for some reason so I couldn't get this working without a small sleep
        time.sleep(0.1)
        print(f'>> [{written}] {input}')
        return written

    def read(self, size, encoding='utf-8') -> str:
        '''
        Reads the serial port until the size is reached or the timeout occurs.\n
        Returns the message as string decoded as utf-8 by defualt. If instead you want
        to read the raw message in bytes, set the encoding to None.
        '''
        if not encoding:
            return self.ser.read(size)

        return self.ser.read(size).decode(encoding)

    def readline(self, size=-1, encoding='utf-8') -> str:
        '''
        Reads the serial port until the end of line character is found or
        the size is reached (-1 means no limit) or the timeout occurs.\n
        Returns the message as string decoded as utf-8 by defualt. If instead you want
        to read the raw message in bytes, set the encoding to None.
        '''
        if not encoding:
            return self.ser.readline(size)

        return self.ser.readline(size).decode(encoding)

    def __del__(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        print('Terminated')
