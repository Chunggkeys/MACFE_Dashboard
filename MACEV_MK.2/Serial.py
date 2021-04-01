from I2C_Accelerometer import AccelerometerI2C
from SPI_Accelerometer_Test import AccelerometerSPI

class Serial:
    I2C = None
    SPI = None
    
    def __init__(self, address=0x68, chip='9250', scalefactor):
        I2C = AccelerometerI2C(address, scalefactor)
        SPI = AccelerometerSPI(chip, scalefactor)

    def testI2C(time):
        I2C.Accelerometer_Data(time)

    def fakeI2C(time):
        pass

    def testSPI(time):
        SPI.Accelerometer_Data(time)

