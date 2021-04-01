import sys
sys.path.append('./uart')

from I2C_Accelerometer import AccelerometerI2C
from SPI_Accelerometer_Test import AccelerometerSPI
from tester import Tester

class Serial:
    I2C: AccelerometerI2C
    SPI: AccelerometerSPI
    UART: Tester
    
    def __init__(self, scalefactor, address=0x68, chip='9250'):
        I2C = AccelerometerI2C(address, scalefactor)
        SPI = AccelerometerSPI(chip, scalefactor)
        UART = Tester()

    def testI2C(time):
        I2C.Accelerometer_Data(time)

    def fakeI2C(time):
        pass

    def testSPI(time):
        SPI.Accelerometer_Data(time)

    def testUART():
        UART.test()   
