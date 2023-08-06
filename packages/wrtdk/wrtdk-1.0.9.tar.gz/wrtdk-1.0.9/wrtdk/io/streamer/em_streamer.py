'''
Created on Oct 31, 2019

@author: reynolds
'''

import os, sys

from wrtdk.io.streamer.streamer import LoggingStreamer
from PyQt5.QtCore import pyqtSignal

class MyClass(LoggingStreamer):
    '''
    classdocs
    '''
    
    EM = 0
    CONF = 1
    GGA = 2
    
    new_timeout = pyqtSignal()# timeout signal
    new_em = pyqtSignal(int,int,list)#type,list length,data
    new_conf = pyqtSignal(int,int,list)#type, list length,data
    new_gga = pyqtSignal(int,int,list)#type, list length, data

    def __init__(self,port=None,debug=False,filename=None,dt=0.1):
        '''
        Constructor
        '''
        super.__init__(debug=debug,port=port,dt=dt)
        
        if self._debug and os.path.join(filename):
            print('Simulation is currently not functional - rwr 10/31/19')
            
    def run(self):
        self.set_mode()
        
        while self._running:
            try:
                msg,addr = self.port.read(1024)
            except Exception as e:
                exc_type, _, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
                self.new_timeout.emit()
                continue