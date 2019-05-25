## presenter.py is a child thread to view.py and takes info from guiModel by using a listener

from PyQt5 import QtWidgets
from multiprocessing.connection import Listener
from PyQt5.QtCore import pyqtSignal, QThread
import sys

## Child thread to view.py, accepts data through socket and passes to view
class Presenter(QThread):

    ## Signal to send to view.py
    updateSignal = pyqtSignal(object)
    ##
    
    def __init__(self, app):
        super().__init__()

        self.app = app

        ## Initializes and runs listener, MUST BE INITIALIZED BEFORE CLIENT
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address, authkey=None)
        ##

    def run(self):
        
        self.connection = self.listener.accept()
        
        ## Starts listener and emits signal to update GUI when data is received
        while 1:    
            self.app.processEvents()
            data = self.connection.recv()
            self.updateSignal.emit(data)
            if data.getShutdown() == 1:

                ## Closes connection on shutdown
                self.connection.close() 
                ##
##
        

        