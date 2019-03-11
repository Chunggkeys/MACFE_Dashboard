import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont 
from PyQt5.QtCore import *

class selectWindow(QWidget):

    ## Signal definitions
    yesClicked = pyqtSignal()
    noClicked = pyqtSignal()
    ##
    
    def __init__(self):
        
        ##Initializes QWidget class
        super().__init__()
        ##

        self.initUI()

    def initUI(self):

        ##Appearance of UI
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("Selection Window")

        self.label = QLabel("Would you like a speedometer?",self)
        self.pyButtonYes = QPushButton("Yes",self)
        self.pyButtonNo = QPushButton("No",self)

        self.label.setAlignment(Qt.AlignCenter)

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
        ##

        ## Signals yesButtonClicked that yes button in window is pressed
        self.pyButtonYes.clicked.connect(self.yesButtonClicked)
        ##

        ## Signal noButtonClicked that no button in window is pressed
        self.pyButtonNo.clicked.connect(self.noButtonClicked)
        ##

        self.show()

    ## Emits signal and closes window
    def yesButtonClicked(self):
        self.yesClicked.emit()
        self.close()

    def noButtonClicked(self):
        self.noClicked.emit()
        self.close()
    ##
    
    ## Defines the grid of the UI and inserts buttons onto coordinates
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()

        rows = 0
        while rows < 4:
            cols = 0
            while cols < 4:
                if rows == 2 and cols == 1:
                    layout.addWidget(self.pyButtonYes, rows, cols)
                elif rows == 2 and cols == 2:
                    layout.addWidget(self.pyButtonNo, rows, cols)
                elif rows == 1 and cols == 1:
                    layout.addWidget(self.label, rows, cols, 1, 2)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
    ##

class MainWindowNoSpeed(QWidget): 

    ## Signal definition
    buttonClicked = pyqtSignal()
    ##

    def __init__(self):
        ## Initializes QWidget class
        super().__init__()
        ##

        self.initUI()

    def initUI(self):
        
        ## Appearance of UI
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("No Speed")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)  
        torqueFont = QFont()
        torqueFont.setPointSize(50)

        self.motorTemperature = QLabel("Motor Temperature", self)
        self.motorTemperature.setAlignment(Qt.AlignCenter)
        self.motorTemperatureIconRed = QPixmap('icons/engineTempRed.jpg')
        self.motorTemperatureIconBlue = QPixmap('icons/engineTempBlue.jpg')
        self.motorTemperatureIconGreen = QPixmap('icons/engineTempGreen.jpg')

        self.speed = QLabel("Speed", self)
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setStyleSheet("QLabel {background-color: green}")

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)
        self.batteryLevel.setStyleSheet("color: white")
        self.batteryLevel.setStyleSheet("QLabel {background-color: green}")

        self.batteryTemperature = QLabel("Battery Temperature", self)
        self.batteryTemperature.setAlignment(Qt.AlignCenter)
        self.batteryTemperature.setStyleSheet("QLabel {background-color: green}")
        self.batteryTemperatureIcon = QPixmap('icons/batteryTempReady.jpg')
        self.batteryTemperatureHighIcon = QPixmap('icons/batteryTempNotReady.jpg')

        self.motorTemperatureLeftFront = QLabel("Motor Temperature LR", self)
        self.motorTemperatureLeftFront.setAlignment(Qt.AlignCenter)
        self.motorTemperatureLeftFront.setStyleSheet("QLabel {background-color: green} ")

        self.motorTemperatureRightFront = QLabel("Motor Temperature RF", self)
        self.motorTemperatureRightFront.setAlignment(Qt.AlignCenter)
        self.motorTemperatureRightFront.setStyleSheet("QLabel {background-color: green} ")

        self.motorTemperatureLeftRear = QLabel("Motor Temperature LR", self)
        self.motorTemperatureLeftRear.setAlignment(Qt.AlignCenter)
        self.motorTemperatureLeftRear.setStyleSheet("QLabel {background-color: green} ")

        self.motorTemperatureRightRear = QLabel("Motor Temperature RR", self)
        self.motorTemperatureRightRear.setAlignment(Qt.AlignCenter)
        self.motorTemperatureRightRear.setStyleSheet("QLabel {background-color: green} ")

        self.motorTemperatureLabel = QLabel("Motor Temperatures", self)
        self.motorTemperatureLabel.setAlignment(Qt.AlignCenter)
        self.motorTemperatureLabel.setStyleSheet("color: white")

        self.highVoltReady = QLabel("HV", self)
        self.highVoltReady.setAlignment(Qt.AlignCenter)
        self.highVoltReady.setStyleSheet("QLabel {background-color: green} ")

        self.lowVoltReady = QLabel("LV", self)
        self.lowVoltReady.setAlignment(Qt.AlignCenter)
        self.lowVoltReady.setStyleSheet("QLabel {background-color: green}")

        self.readyLabel = QLabel("Startup Status", self)
        self.readyLabel.setAlignment(Qt.AlignCenter)
        self.readyLabel.setStyleSheet('color: white')

        self.shutdown = QLabel("Shutdown",self)
        self.shutdown.setAlignment(Qt.AlignCenter)
        self.shutdownIcon = QPixmap('icons/shutdown.jpeg')

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
        ##

    ## Widget behavior based on passed values
    def processValues(self, values):
        # if int(values[0]) > 80: 
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconRed)
        # elif int(values[0]) < 60:
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconBlue)
        # else:
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconGreen)
        
        # if int(values[3]) > 70:
        #     self.batteryTemperature.setPixmap(self.batteryTemperatureHighIcon)
        # else:
        #     self.batteryTemperature.setPixmap(self.batteryTemperatureIcon)
        
        # if int(values[8]) == 1:
        #     self.shutdown.setPixmap(self.shutdownIcon)
        # else:
        #     self.shutdown.clear()

        self.changeText(values)
    ##
    
    ## For labels that require the showing of values, this method updates labels
    def changeText(self, values):
        self.batteryLevel.setText(values[2])
        # self.motorTorque.setText(values[4])
        self.motorTemperature.setText(values[0])
        self.shutdown.setText(values[8])
        self.batteryTemperature.setText(values[3])
    ##

    ## Defines the grid of the UI and inserts widgets onto coordinates
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()

        rows = 0
        while rows < 15:
            cols = 0
            while cols < 15:
                if rows == 1 and cols == 1:
                    layout.addWidget(self.batteryTemperature, rows, cols,1,7)
                elif rows == 3 and cols == 1:
                    layout.addWidget(self.batteryLevel,rows,cols,6,7)
                elif rows == 10 and cols == 1:
                    layout.addWidget(self.speed,rows,cols,4,7)
                elif rows == 0 and cols == 12:
                    layout.addWidget(self.motorTemperatureLabel,rows,cols,1,3)
                elif rows == 1 and cols == 12:
                    layout.addWidget(self.motorTemperatureLeftFront,rows,cols,3,1)
                elif rows == 1 and cols == 14:
                    layout.addWidget(self.motorTemperatureRightFront,rows,cols,3,1)
                elif rows == 5 and cols == 12:
                    layout.addWidget(self.motorTemperatureLeftRear,rows,cols,3,1)
                elif rows == 5 and cols == 14:
                    layout.addWidget(self.motorTemperatureRightRear,rows,cols,3,1)
                elif rows == 9 and cols == 12:
                    layout.addWidget(self.readyLabel,rows,cols,1,3)
                elif rows == 10 and cols == 12:
                    layout.addWidget(self.highVoltReady,rows,cols)
                elif rows == 10 and cols == 14:
                    layout.addWidget(self.lowVoltReady,rows,cols)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
    ##

class MainWindowSpeed(QWidget):

    def __init__(self):
        ## Initialize QWidget class
        super().__init__()
        ##

        self.initUI()
    
    def initUI(self):

        ## Appearance of UI
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("With Speed")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        speedFont = QFont()
        speedFont.setPointSize(35)

        self.motorTemperature = QLabel("Motor Temperature", self)
        self.motorTemperature.setAlignment(Qt.AlignCenter)
        self.motorTemperatureIconRed = QPixmap("icons/engineTempRed.jpg")
        self.motorTemperatureIconBlue = QPixmap("icons/engineTmepBlue.jpg")
        self.motorTemperatureIconGreen = QPixmap('icons/engineTempGreen.jpg')

        self.speed = QProgressBar(self)
        self.speed.setMaximum(80)
        self.speed.setValue(50)
        self.speed.setTextVisible(False)

        self.speedDisplay = QLabel("Speed", self)
        self.speedDisplay.setStyleSheet('color: white')
        self.speedDisplay.setAlignment(Qt.AlignCenter)
        self.speedDisplay.setFont(speedFont)

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)
        
        self.batteryTemperature = QLabel("Battery Temperature", self)
        self.batteryTemperature.setAlignment(Qt.AlignCenter)
        self.batteryTemperatureIcon = QPixmap('icons/batteryTempReady.jpg')
        self.batteryTemperatureHighIcon = QPixmap('icons/batteryTempNotReady.jpg')

        self.motorTorqueLeftFront = QLabel("Motor Torque LR", self)
        self.motorTorqueLeftFront.setAlignment(Qt.AlignCenter)

        self.motorTorqueRightFront = QLabel("Motor Torque RF", self)
        self.motorTorqueRightFront.setAlignment(Qt.AlignCenter)

        self.motorTorqueLeftRear = QLabel("Motor Torque LR", self)
        self.motorTorqueLeftRear.setAlignment(Qt.AlignCenter)

        self.motorTorqueRightRear = QLabel("Motor Torque RR", self)
        self.motorTorqueRightRear.setAlignment(Qt.AlignCenter)

        
        self.shutdown = QLabel("Shutdown", self)
        self.shutdown.setAlignment(Qt.AlignCenter)
        self.shutdownIcon = QPixmap("icons/shutdown.jpeg")

        

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
        ##
    
    ## Defines the grid of the UI and inserts widgets onto coordinates
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()
        
        rows = 0
        while rows < 15:
            cols = 0
            while cols < 15:
                if rows == 2 and cols == 1:
                    layout.addWidget(self.batteryLevel, rows, cols)
                elif rows == 1 and cols == 0:
                    layout.addWidget(self.speedDisplay, rows, cols, 1,3)
                elif rows == 5 and cols == 0:
                    layout.addWidget(self.speed, rows, cols, 8, 3)
                elif rows == 3 and cols == 0:
                    layout.addWidget(self.batteryTemperature, rows, cols)
                elif rows == 3 and cols == 1:
                    layout.addWidget(self.shutdown, rows, cols)
                elif rows == 3 and cols == 2:
                    layout.addWidget(self.motorTemperature,rows,cols)
                # elif rows == 4 and cols == 1:
                #     layout.addWidget(self.motorTorque,rows,cols)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
    ##
    
    ## Widget behavior based on passed values
    def processValues(self, values):

        # if int(values[0]) > 80: 
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconRed)
        # elif int(values[0]) < 60:
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconBlue)
        # else:
        #     self.motorTemperature.setPixmap(self.motorTemperatureIconGreen)
        
        # if int(values[3]) > 70:
        #     self.batteryTemperature.setPixmap(self.batteryTemperatureHighIcon)
        # else:
        #     self.batteryTemperature.setPixmap(self.batteryTemperatureIcon)
        
        # if int(values[8]) == 1:
        #     self.shutdown.setPixmap(self.shutdownIcon)
        # else:
        #     self.shutdown.clear()

        self.changeText(values)
    ##
    
    ## For labels that require the showing of values, this method updates labels
    def changeText(self, values):
        self.batteryLevel.setText(values[2])
        #self.motorTorque.setText(values[4])
        self.speed.setValue(int(values[1]))
        self.speedDisplay.setText(values[1])
    ##