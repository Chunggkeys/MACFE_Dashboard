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

        # ## Signals yesButtonClicked that yes button in window is pressed
        # self.pyButtonYes.clicked.connect(self.yesButtonClicked)
        # ##

        ## Signal noButtonClicked that no button in window is pressed
        self.pyButtonNo.clicked.connect(self.noButtonClicked)
        ##

        self.show()

    ## Emits signal and closes window
    # def yesButtonClicked(self):
    #     self.yesClicked.emit()
    #     self.close()

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

class MainWindow(QWidget): 

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
        self.setWindowTitle("Dashboard")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)  
        torqueFont = QFont()
        torqueFont.setPointSize(50)
        shutdownFont = QFont()
        shutdownFont.setPointSize(100)
        # batteryLevelFont = QFont()
        # batteryLevelFont.setPointSize(50)

        self.speed = QLabel("Speed", self)
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setStyleSheet("QLabel {background-color: green}")

        self.batteryLevel = QLabel("Battery Level", self)
        self.batteryLevel.setAlignment(Qt.AlignCenter)
        # self.batteryLevel.setFont(batteryLevelFont)
        self.batteryLevel.setStyleSheet("color: white")
        self.batteryLevel.setStyleSheet("QLabel {background-color: green}")

        self.batteryTemperatureError = QLabel("Battery Temp Icon", self)
        self.batteryTemperatureError.setAlignment(Qt.AlignCenter)
        self.batteryTemperatureError.setStyleSheet("QLabel {background-color: green}")
        self.batteryTemperatureIcon = QPixmap('icons/iconJPGFiles/batteryTempRed.jpg')

        self.batteryTemperature = QProgressBar(self)
        self.batteryTemperature.setMaximum(100)
        self.batteryTemperature.setMinimum(0)
        self.batteryTemperature.setTextVisible(False)

        self.batteryTemperatureLabel = QLabel("Battery Temperature", self)
        self.batteryTemperatureLabel.setAlignment(Qt.AlignCenter)
        self.batteryTemperatureLabel.setStyleSheet("color: white")

        self.motorTemperatureLeftFront = QProgressBar(self)
        self.motorTemperatureLeftFront.setOrientation(Qt.Vertical)
        self.motorTemperatureLeftFront.setMaximum(100)
        self.motorTemperatureLeftFront.setMinimum(0)

        self.motorTemperatureError = QLabel("Motor Temp Icon", self)
        self.motorTemperatureError.setAlignment(Qt.AlignCenter)
        self.motorTemperatureError.setStyleSheet("QLabel {background-color: green}")
        self.motorTemperatureIcon = QPixmap('icons/iconJPGFiles/motorTempRed.jpg')

        self.motorTemperatureRightFront = QProgressBar(self)
        self.motorTemperatureRightFront.setOrientation(Qt.Vertical)
        self.motorTemperatureRightFront.setMaximum(100)
        self.motorTemperatureRightFront.setMinimum(0)

        self.motorTemperatureLeftRear = QProgressBar(self)
        self.motorTemperatureLeftRear.setOrientation(Qt.Vertical)
        self.motorTemperatureLeftRear.setMaximum(100)
        self.motorTemperatureLeftRear.setMinimum(0)

        self.motorTemperatureRightRear = QProgressBar(self)
        self.motorTemperatureRightRear.setOrientation(Qt.Vertical)
        self.motorTemperatureRightRear.setMaximum(100)
        self.motorTemperatureRightRear.setMinimum(0)

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

        self.outputLog = QLabel("Output log", self)
        self.outputLog.setAlignment(Qt.AlignCenter)
        self.outputLog.setStyleSheet("QLabel {background-color: green}")

        self.createGrid()

        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)
        ##

    ## Widget behavior based on passed values
    def processValues(self, values):
        
        self.progressBarColors(values)

        if int(values[2]) > 70:
            self.batteryTemperatureError.setScaledContents(True)
            self.batteryTemperatureError.setPixmap(self.batteryTemperatureIcon)
        
        # if int(values[8]) == 1:
        #     self.shutdown.setPixmap(self.shutdownIcon)
        # else:
        #     self.shutdown.clear()

        self.changeTextAndValue(values)
    ##

    ## Method dedicated to process Motor Temperature values
    def progressBarColors(self,values):

        if values[2] > 80: 
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.red)
        elif values[2] > 60:
            self.changeProgressBarColor(self.batteryTemperature, QtGui.QColor(255,143,15))
        elif values[2] > 40:
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.yellow)
        elif values[2] > 20:    
            self.changeProgressBarColor(self.batteryTemperature, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.batteryTemperature, QtCore.Qt.green)
        
        if values[3] > 80: 
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.red)
        elif values[3] > 60:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtGui.QColor(255,143,15))
        elif values[3] > 40:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.yellow)
        elif values[3] > 20:    
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureLeftFront, QtCore.Qt.green)

        if values[4] > 80: 
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.red)
        elif values[4] > 60:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtGui.QColor(255,143,15))
        elif values[4] > 40:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.yellow)
        elif values[4] > 20:    
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureRightFront, QtCore.Qt.green)
        
        if values[5] > 80: 
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.red)
        elif values[5] > 60:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtGui.QColor(255,143,15))
        elif values[5] > 40:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.yellow)
        elif values[5] > 20:    
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureLeftRear, QtCore.Qt.green)
        
        if values[6] > 80: 
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.red)
        elif values[6] > 60:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtGui.QColor(255,143,15))
        elif values[6] > 40:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.yellow)
        elif values[6] > 20:    
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtGui.QColor(226,255,41,255))
        else:
            self.changeProgressBarColor(self.motorTemperatureRightRear, QtCore.Qt.green)
    ##

    def changeProgressBarColor(self, progressBar, color):
        palette = QtGui.QPalette(progressBar.palette())
        palette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(color))
        progressBar.setPalette(palette)

    ## For labels that require the showing of values, this method updates labels
    def changeTextAndValue(self, values):
        self.batteryLevel.setText(str(values[1]))
        self.batteryTemperature.setValue(values[2])
        self.motorTemperatureLeftFront.setValue(values[3])
        self.motorTemperatureRightFront.setValue(values[4])
        self.motorTemperatureLeftRear.setValue(values[5])
        self.motorTemperatureRightRear.setValue(values[6])
    ##

    ## Defines the grid of the UI and inserts widgets onto coordinates
    def createGrid(self):

        self.groupBox = QGroupBox()
        layout = QGridLayout()

        rows = 0
        while rows < 15:
            cols = 0
            while cols < 15:
                if rows == 1 and cols == 0:
                    layout.addWidget(self.batteryTemperature, rows, cols,1,7)
                elif rows == 1 and cols == 8:
                    layout.addWidget(self.batteryTemperatureError,rows,cols,2,2)
                elif rows == 0 and cols == 0:
                    layout.addWidget(self.batteryTemperatureLabel,rows,cols,1,7)
                elif rows == 3 and cols == 0:
                    layout.addWidget(self.batteryLevel,rows,cols,6,7)
                elif rows == 10 and cols == 0:
                    layout.addWidget(self.speed,rows,cols,4,7)
                elif rows == 4 and cols == 8:
                    layout.addWidget(self.motorTemperatureError,rows,cols,2,2)
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
                elif rows == 12 and cols == 8:
                    layout.addWidget(self.outputLog,rows,cols,2,7)
                else:
                    layout.addWidget(QLabel("",self), rows, cols)
                cols += 1
            rows += 1

        self.groupBox.setLayout(layout)
    ##