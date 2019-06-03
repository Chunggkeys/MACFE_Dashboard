from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import *
import sys

class FadeOutTrial(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Fade Out Sample")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.logo = QPixmap("MFELogoBlackBackground.png")

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.logo)
        
        self.createGrid()
    
        box = QVBoxLayout()
        box.addWidget(self.groupBox)
        self.setLayout(box)

        QTimer.singleShot(3000,self.doFade)

        # self.doFade()
    
    def doFade(self):
        self.effect = QGraphicsOpacityEffect(self)
        self.label.setGraphicsEffect(self.effect)
        self.propertyAnimation = QPropertyAnimation(self.effect, b"opacity")
        self.propertyAnimation.setDuration(5000)
        self.propertyAnimation.setStartValue(1)
        self.propertyAnimation.setEndValue(0)
        self.propertyAnimation.setEasingCurve(QEasingCurve.OutBack)
        self.propertyAnimation.start(QPropertyAnimation.DeleteWhenStopped)

    def createGrid(self):
        self.groupBox = QGroupBox()
        layout = QGridLayout()

        rows = 0
        while rows < 3:
            cols = 0
            while cols < 3:
                if rows == 1 and cols == 1:
                    layout.addWidget(self.label,rows,cols)
                else:
                    layout.addWidget(QLabel(self),rows,cols)       
                cols += 1
            rows += 1 

        self.groupBox.setLayout(layout)
    

    
app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

window = FadeOutTrial()
window.showMaximized()
window.show()

app.exec_()

