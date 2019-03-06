import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont 
from PyQt5.QtCore import *

class selectWindow(QWidget):

    yesClicked = pyqtSignal()
    noClicked = pyqtSignal()
    #testClicked = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

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

        self.pyButtonYes.clicked.connect(self.yesButtonClicked)
        self.pyButtonNo.clicked.connect(self.noButtonClicked)

        self.show()

    def yesButtonClicked(self):
        self.yesClicked.emit()
        self.close()

    def noButtonClicked(self):
        self.noClicked.emit()
        self.close()
    
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

class MainWindowNoSpeed(QWidget): 

    buttonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
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

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)

        self.batteryTemperature = QLabel("Battery Temperature", self)
        self.batteryTemperature.setAlignment(Qt.AlignCenter)
        self.batteryTemperatureIcon = QPixmap('icons/batteryTempReady.jpg')
        self.batteryTemperatureHighIcon = QPixmap('icons/batteryTempNotReady.jpg')

        self.motorTorque = QLabel("Motor Torque",self)
        self.motorTorque.setAlignment(Qt.AlignCenter)
        self.motorTorque.setFont(torqueFont)

        self.shutdown = QLabel("Shutdown",self)
        self.shutdown.setAlignment(Qt.AlignCenter)
        self.shutdownIcon = QPixmap('icons/shutdown.jpeg')

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)


        self.motorTemperature.setStyleSheet('color: blue')
        self.batteryLevel.setStyleSheet('color: white')
        self.batteryTemperature.setStyleSheet('color: white')
        self.motorTorque.setStyleSheet('color: white')
        

    def processValues(self, values):
        if int(values[0]) > 80: 
            self.motorTemperature.setPixmap(self.motorTemperatureIconRed)
        elif int(values[0]) < 60:
            self.motorTemperature.setPixmap(self.motorTemperatureIconBlue)
        else:
            self.motorTemperature.setPixmap(self.motorTemperatureIconGreen)
        
        if int(values[3]) > 70:
            self.batteryTemperature.setPixmap(self.batteryTemperatureHighIcon)
        else:
            self.batteryTemperature.setPixmap(self.batteryTemperatureIcon)
        
        if int(values[5]) == 1:
            self.shutdown.setPixmap(self.shutdownIcon)
        else:
            self.shutdown.clear()

        self.changeText(values)
    
    def changeText(self, values):
        self.batteryLevel.setText(values[2])
        self.motorTorque.setText(values[4])

    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()

        rows = 0
        while rows < 3:
            cols = 0
            while cols < 3:
                if rows == 0 and cols == 1:
                    layout.addWidget(self.batteryLevel, rows, cols)
                elif rows == 1 and cols == 0:
                    layout.addWidget(self.batteryTemperature, rows, cols)
                elif rows == 1 and cols == 1:
                    layout.addWidget(self.shutdown, rows, cols)
                elif rows == 1 and cols == 2:
                    layout.addWidget(self.motorTemperature,rows,cols)
                elif rows == 2 and cols == 1:
                    layout.addWidget(self.motorTorque,rows,cols)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)

class MainWindowSpeed(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("With Speed")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        speedFont = QFont()
        speedFont.setPointSize(35)

        self.motorTemperature = QLabel("Motor Temperature", self)
        self.motorTemperature.setAlignment(Qt.AlignCenter)
        #self.motorTemperature.move(50,50)
        self.motorTemperatureIconRed = QPixmap("icons/engineTempRed.jpg")
        self.motorTemperatureIconBlue = QPixmap("icons/engineTmepBlue.jpg")
        self.motorTemperatureIconGreen = QPixmap('icons/engineTempGreen.jpg')

        self.speed = QProgressBar(self)
        self.speed.setMaximum(80)
        self.speed.setValue(50)
        self.speed.setTextVisible(False)
        #self.speed.move(100,100)

        self.speedDisplay = QLabel("Speed", self)
        self.speedDisplay.setStyleSheet('color: white')
        self.speedDisplay.setAlignment(Qt.AlignCenter)
        self.speedDisplay.setFont(speedFont)

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)
        #self.batteryLevel.move(150,150)

        self.batteryTemperature = QLabel("Battery Temperature", self)
        self.batteryTemperature.setAlignment(Qt.AlignCenter)
        #self.batteryTemperature.move(200,200)
        self.batteryTemperatureIcon = QPixmap('icons/batteryTempReady.jpg')
        self.batteryTemperatureHighIcon = QPixmap('icons/batteryTempNotReady.jpg')

        self.motorTorque = QLabel("Motor Torque", self)
        self.motorTorque.setAlignment(Qt.AlignCenter)
        #self.motorTorque.move(250,250)

        self.shutdown = QLabel("Shutdown", self)
        self.shutdown.setAlignment(Qt.AlignCenter)
        #self.shutdown.move(300,300)
        self.shutdownIcon = QPixmap("icons/shutdown.jpeg")

        

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
    
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()
        
        rows = 0
        while rows < 6:
            cols = 0
            while cols < 3:
                if rows == 2 and cols == 1:
                    layout.addWidget(self.batteryLevel, rows, cols)
                elif rows == 1 and cols == 0:
                    layout.addWidget(self.speedDisplay, rows, cols, 1,3)
                elif rows == 0 and cols == 0:
                    layout.addWidget(self.speed, rows, cols, 1, 3)
                elif rows == 3 and cols == 0:
                    layout.addWidget(self.batteryTemperature, rows, cols)
                elif rows == 3 and cols == 1:
                    layout.addWidget(self.shutdown, rows, cols)
                elif rows == 3 and cols == 2:
                    layout.addWidget(self.motorTemperature,rows,cols)
                elif rows == 4 and cols == 1:
                    layout.addWidget(self.motorTorque,rows,cols)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
        
    def processValues(self, values):

        if int(values[0]) > 80: 
            self.motorTemperature.setPixmap(self.motorTemperatureIconRed)
        elif int(values[0]) < 60:
            self.motorTemperature.setPixmap(self.motorTemperatureIconBlue)
        else:
            self.motorTemperature.setPixmap(self.motorTemperatureIconGreen)
        
        if int(values[3]) > 70:
            self.batteryTemperature.setPixmap(self.batteryTemperatureHighIcon)
        else:
            self.batteryTemperature.setPixmap(self.batteryTemperatureIcon)
        
        if int(values[5]) == 1:
            self.shutdown.setPixmap(self.shutdownIcon)
        else:
            self.shutdown.clear()

        self.changeText(values)
    
    def changeText(self, values):
        self.batteryLevel.setText(values[2])
        self.motorTorque.setText(values[4])
        self.speed.setValue(int(values[1]))
        self.speedDisplay.setText(values[1])