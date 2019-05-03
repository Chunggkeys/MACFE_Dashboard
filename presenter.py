## presenter.py is a child thread to view.py and takes info from guiModel by using a listener

from PyQt5 import QtWidgets
from multiprocessing.connection import Listener
from PyQt5.QtCore import pyqtSignal, QThread
import sys

class Presenter(QThread):

    updateSignal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address, authkey=None)

    def run(self):
        
        self.connection = self.listener.accept()
        
        ## Starts listener and emits signal to update GUI when data is received
        while 1:    
            data = self.connection.recv()
            self.updateSignal.emit(data)
            if data.getShutdown() == 1:
                self.connection.close()

    # def updateGUI(self,data):
    #     self.mainWindow.processValues(data)
