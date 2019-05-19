import sys
from presenter import Presenter
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont, QFontDatabase 
from PyQt5.QtCore import *
from PyQt5 import *

##Error Window class
class ShutdownWindow(QWidget):

    def __init__(self):
        super().__init__()
    
        self.initUI()
    
    def initUI(self):
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("ERROR")
        print("Shutdown")	

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        
        self.font = QFont()
        self.font.setPointSize(150)

        self.label = QLabel("Error", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red")
        self.label.setFont(self.font)
    
        self.groupBox = QGroupBox()
        self.layout = QGridLayout()

        self.layout.addWidget(self.label,0,0)
        self.groupBox.setLayout(self.layout)

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
##

        
class MainWindow(QWidget): 

    ## Signal definition
    buttonClicked = pyqtSignal()
    ##

    def __init__(self, presenter):
        ## Initializes QWidget class as parent
        super().__init__()
        ##
        
        self.presenter = presenter
        self.presenter.start()
        self.presenter.updateSignal.connect(self.processValues)

        self.initUI()

    def initUI(self):
        
        ## Appearance of UI
        self.setWindowTitle("Dashboard")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)  
    

        progressBarWidthScale = 1.1
        progressBarTextState = False

        motorTemperatureMinimum = -20
        motorTemperatureMaximum = 235

        QFontDatabase.addApplicationFont('font/DS-DIGI.TTF')

        labelFont = QFont("DS-Digital")
        labelFont.setPointSize(18)

        torqueFont = QFont()
        torqueFont.setPointSize(50)

        speedFont = QFont("DS-Digital")
        speedFont.setPointSize(90)

        shutdownFont = QFont("DS-Digital")
        shutdownFont.setPointSize(100)

        batteryLevelFont = QFont("DS-Digital")
        batteryLevelFont.setPointSize(90)

        self.speed = QLabel("Speed", self)
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setFont(speedFont)
        self.speed.setStyleSheet("color: white")

        self.batteryTemperature = QProgressBar(self)
        self.batteryTemperature.setFixedHeight(progressBarWidthScale*self.batteryTemperature.width())
        self.batteryTemperature.setMaximum(100)
        self.batteryTemperature.setMinimum(0)
        self.batteryTemperature.setTextVisible(False)
        
        self.batteryTemperatureLabel = QLabel("Battery Temperature", self)
        self.batteryTemperatureLabel.setFont(labelFont)
        self.batteryTemperatureLabel.setAlignment(Qt.AlignCenter)
        self.batteryTemperatureLabel.setStyleSheet("color: white")

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)
        self.batteryLevel.setFont(batteryLevelFont)
        self.batteryLevel.setStyleSheet("color: white")

        self.batteryTemperatureError = QLabel("Battery Temp Icon", self)
        self.batteryTemperatureError.setAlignment(Qt.AlignCenter)

        self.motorTemperatureLeftFront = QProgressBar(self)
        self.motorTemperatureLeftFront.setTextVisible(progressBarTextState)
        self.motorTemperatureLeftFront.setOrientation(Qt.Vertical)
        self.motorTemperatureLeftFront.setFixedWidth(progressBarWidthScale*self.motorTemperatureLeftFront.width())
        self.motorTemperatureLeftFront.setMaximum(motorTemperatureMaximum)
        self.motorTemperatureLeftFront.setMinimum(motorTemperatureMinimum)

        self.motorTemperatureError = QLabel("Motor Temp Icon", self)
        self.motorTemperatureError.setAlignment(Qt.AlignCenter)

        self.motorTemperatureRightFront = QProgressBar(self)
        self.motorTemperatureRightFront.setTextVisible(progressBarTextState)
        self.motorTemperatureRightFront.setOrientation(Qt.Vertical)
        self.motorTemperatureRightFront.setFixedWidth(progressBarWidthScale*self.motorTemperatureRightFront.width())
        self.motorTemperatureRightFront.setMaximum(motorTemperatureMaximum)
        self.motorTemperatureRightFront.setMinimum(motorTemperatureMinimum)

        self.motorTemperatureLeftRear = QProgressBar(self)
        self.motorTemperatureLeftRear.setTextVisible(progressBarTextState)
        self.motorTemperatureLeftRear.setOrientation(Qt.Vertical)
        self.motorTemperatureLeftRear.setFixedWidth(progressBarWidthScale*self.motorTemperatureLeftRear.width())
        self.motorTemperatureLeftRear.setMaximum(motorTemperatureMaximum)
        self.motorTemperatureLeftRear.setMinimum(motorTemperatureMinimum)

        self.motorTemperatureRightRear = QProgressBar(self)
        self.motorTemperatureRightRear.setTextVisible(progressBarTextState)
        self.motorTemperatureRightRear.setOrientation(Qt.Vertical)
        self.motorTemperatureRightRear.setFixedWidth(progressBarWidthScale*self.motorTemperatureRightRear.width())
        self.motorTemperatureRightRear.setMaximum(motorTemperatureMaximum)
        self.motorTemperatureRightRear.setMinimum(motorTemperatureMinimum)

        self.motorTemperatureLabel = QLabel("Motor Temperatures", self)
        self.motorTemperatureLabel.setFont(labelFont)
        self.motorTemperatureLabel.setAlignment(Qt.AlignCenter)
        self.motorTemperatureLabel.setStyleSheet("color: white")

        self.highVoltReady = QLabel("HV", self)
        self.highVoltReady.setFont(labelFont)
        self.highVoltReady.setAlignment(Qt.AlignCenter)
        self.highVoltReady.setStyleSheet("color: white")
        
        self.lowVoltReady = QLabel("LV", self)
        self.lowVoltReady.setFont(labelFont)
        self.lowVoltReady.setAlignment(Qt.AlignCenter)
        self.lowVoltReady.setStyleSheet("color: white")

        self.readyLabel = QLabel("Startup Status", self)
        self.readyLabel.setFont(labelFont)
        self.readyLabel.setAlignment(Qt.AlignCenter)
        self.readyLabel.setStyleSheet('color: white')
    
        self.shutdown = QLabel("Shutdown",self)
        self.shutdown.setAlignment(Qt.AlignCenter)
        self.shutdownIcon = QPixmap('icons/shutdown.jpeg')

        self.maxPowerLabel = QLabel("Max Power Available")
        self.maxPowerLabel.setAlignment(Qt.AlignCenter)
        self.maxPowerLabel.setFont(labelFont)
        self.maxPowerLabel.setStyleSheet("color: white")

        self.maxPowerAvailable = QProgressBar(self)
        self.maxPowerAvailable.setFixedHeight(progressBarWidthScale*self.maxPowerAvailable.width())
        self.maxPowerAvailable.setMaximum(100)
        self.maxPowerAvailable.setMinimum(0)
        self.maxPowerAvailable.setTextVisible(progressBarTextState)

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
        ##
    

    ## Widget behavior based on passed values
    def processValues(self, data):
        
        self.progressBarColors(data)

        if data.getHV() == 1:
            self.highVoltReady.setStyleSheet("QLabel {background-color: green}")
        else:
            self.highVoltReady.setStyleSheet("QLabel {background-color: black}")
            self.highVoltReady.setStyleSheet("color: white")
        
        if data.getLV() == 1:
            self.lowVoltReady.setStyleSheet("QLabel {background-color: green}")
        else:
            self.lowVoltReady.setStyleSheet("QLabel {background-color: black}")
            self.lowVoltReady.setStyleSheet("color: white")
        
        if data.getShutdown() == 1:
            self.systemShutdown()

        self.changeTextAndValue(data)
    ##

    ## Opens Error GUI
    def systemShutdown(self):
        print("Shutdown")
        self.hide()
        self.shutdownWindow = ShutdownWindow()
        self.shutdownWindow.showMaximized()
        self.shutdownWindow.show()
    ##
    
    ## Method dedicated to process Motor Temperature values and change progress bar
    def progressBarColors(self,data):

        if  data.getBatteryTemperature() > 80: 
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.red)       
        elif data.getBatteryTemperature() > 60:
            self.changeProgressBarColor(self.batteryTemperature, QtGui.QColor(255,143,15))
        elif data.getBatteryTemperature() > 40:
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.yellow)
        elif data.getBatteryTemperature() > 20:
            self.changeProgressBarColor(self.batteryTemperature, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.green)
        
        if data.getMotorTemperatureOne() > 80: 
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.red)
        elif data.getMotorTemperatureOne() > 60:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtGui.QColor(255,143,15))
        elif data.getMotorTemperatureOne() > 40:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.yellow)
        elif data.getMotorTemperatureOne() > 20:    
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.green)

        if data.getMotorTemperatureTwo() > 80: 
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.red)
        elif data.getMotorTemperatureTwo() > 60:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtGui.QColor(255,143,15))
        elif data.getMotorTemperatureTwo() > 40:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.yellow)
        elif data.getMotorTemperatureTwo() > 20:    
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.green)
        
        if data.getMotorTemperatureThree() > 80: 
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.red)
        elif data.getMotorTemperatureThree() > 60:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtGui.QColor(255,143,15))
        elif data.getMotorTemperatureThree() > 40:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.yellow)
        elif data.getMotorTemperatureThree() > 20:    
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.green)
        
        if data.getMotorTemperatureFour() > 80: 
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.red)
        elif data.getMotorTemperatureFour() > 60:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtGui.QColor(255,143,15))
        elif data.getMotorTemperatureFour() > 40:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.yellow)
        elif data.getMotorTemperatureFour() > 20:    
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.green)

        if data.getMaxPower() < 20: 
            self.changeProgressBarColor(self.maxPowerAvailable, QtCore.Qt.red)
        elif data.getMaxPower() < 40:
            self.changeProgressBarColor(self.maxPowerAvailable, QtGui.QColor(255,143,15))
        elif data.getMaxPower() < 60:
            self.changeProgressBarColor(self.maxPowerAvailable, QtCore.Qt.yellow)
        elif data.getMaxPower() < 80:    
            self.changeProgressBarColor(self.maxPowerAvailable, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.maxPowerAvailable, QtCore.Qt.green)
    ##

    ## Change progress bar color
    def changeProgressBarColor(self, progressBar, color):
        palette = QtGui.QPalette(progressBar.palette())
        palette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(color))
        progressBar.setPalette(palette)
    ##

    ## For labels that require the showing of values, this method updates labels
    def changeTextAndValue(self, data):
        self.batteryLevel.setText("SOC: " + data.getBatteryLevel() + "%")
        self.speed.setText(data.getSpeed() + "<sub>km/h</sub>")
        self.batteryTemperature.setValue(data.getBatteryTemperature())
        self.motorTemperatureLeftFront.setValue(data.getMotorTemperatureOne())
        self.motorTemperatureRightFront.setValue(data.getMotorTemperatureTwo())
        self.motorTemperatureLeftRear.setValue(data.getMotorTemperatureThree())
        self.motorTemperatureRightRear.setValue(data.getMotorTemperatureFour())
        self.maxPowerAvailable.setValue(data.getMaxPower())
    ##

    ## Defines the grid of the UI and inserts widgets onto coordinates
    #  Note that size of widgets are adjusted dynamically by QT based on dimensions of GUI
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()
        subLayout = QGridLayout()
        motorLayout = QGridLayout()
        batteryTemperatureLayout = QGridLayout()
        maxPowerAvailableLayout = QGridLayout()

        rows = 0
        while rows < 15:
            cols = 0
            while cols < 15:
                if rows == 0 and cols == 0:
                    layout.addLayout(batteryTemperatureLayout,rows,cols,3,7)
                    batteryTemperatureLayout.addWidget(self.batteryTemperatureLabel,0,0,1,7)
                    batteryTemperatureLayout.addWidget(self.batteryTemperature,2,0,1,7)
                elif rows == 1 and cols == 8:
                    layout.addWidget(self.batteryTemperatureError,rows,cols,2,2)
                elif rows == 3 and cols == 0:
                    layout.addWidget(self.batteryLevel,rows,cols,8,7)
                elif rows == 11 and cols == 0:
                    layout.addLayout(maxPowerAvailableLayout,rows,cols,3,7)
                    maxPowerAvailableLayout.addWidget(self.maxPowerLabel,0,0,1,7)
                    maxPowerAvailableLayout.addWidget(self.maxPowerAvailable,2,0,1,7)
                elif rows == 4 and cols == 8:
                    layout.addWidget(self.motorTemperatureError,rows,cols,2,2)
                elif rows == 0 and cols == 12:
                    layout.addWidget(self.motorTemperatureLabel,rows,cols,1,3)
                elif rows == 1 and cols == 12:
                    layout.addLayout(motorLayout,rows,cols,7,3)
                    motorLayout.addWidget(self.motorTemperatureLeftFront,0,0,3,1)
                    motorLayout.addWidget(self.motorTemperatureRightFront,0,2,3,1)
                    motorLayout.addWidget(QLabel("",self),3,0,1,3)
                    motorLayout.addWidget(self.motorTemperatureLeftRear,4,0,3,1)
                    motorLayout.addWidget(self.motorTemperatureRightRear,4,2,3,1)
                elif rows == 0 and cols == 9:
                    layout.addWidget(self.readyLabel,rows,cols,1,2)
                elif rows == 1 and cols == 9:
                    layout.addLayout(subLayout,rows,cols,3,2)
                    subLayout.addWidget(self.highVoltReady,0,0)
                    subLayout.addWidget(self.lowVoltReady,1,0)
                elif rows == 12 and cols == 8:
                    layout.addWidget(self.speed,rows,cols,2,7)
                else:
                    layout.addWidget(QLabel("",self),rows,cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
    ##

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

p = Presenter()

window = MainWindow(p)
window.showMaximized()
window.show()

sys.exit(app.exec_())
