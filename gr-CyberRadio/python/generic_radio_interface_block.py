
import logging

import CyberRadioDriver as crd


class generic_radio_interface_block():
    
    def __init__(self,*args,**kwargs):
        self.log = logging.getLogger(self._name)
        self.log.setLevel(logging.DEBUG if kwargs.get("debug",False) else logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s :: %(name)s(%(levelname)s) :: %(message)s'))
        self.log.addHandler( handler )
    
    def initRadioConnection(self,):
        self.log.debug("initRadioConnection")
        self.radioObj = self.radioParam.get("obj",None)
        if self.radioObj is None:
            self.log.debug("Creating radio object")
            self.radioObj = crd.getRadioObject(self.radioParam["type"])
        if not self.radioObj.isConnected():
            self.log.debug("Connecting to radio...")
            if all( self.radioParam.has_key(i) for i in ("host","port") ):
                self.radioObj.connect( "tcp", self.radioParam["host"], self.radioParam["port"] )
            elif all( self.radioParam.has_key(i) for i in ("device","baudrate") ):
                self.radioObj.connect( "tty", self.radioParam["device"], self.radioParam["baudrate"] )
            else:
                raise Exception("%s :: Can't connect to radio"%(self._name))
        if self.radioObj.isConnected():
            self.log.info("Connected to radio!")
    
    def start(self):
        self.log.debug("start")
        self.initRadioConnection()
        self.updateConfig()
        self._init = False
    
        ## Setter & getter for radioParam
    def set_radioParam(self, radioParam={"type":"ndr308","host":"ndr308","port":8617,"obj":None}):
        if self._init or not hasattr(self, "radioParam"):
            self.radioParam = radioParam
            self.radioType = self.radioParam.get("type")
            print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
        elif radioParam!=self.radioParam:
            print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
            self.radioParam = radioParam
            self.updateConfig("radioParam")

    def get_radioParam(self,):
        return self.radioParam
    
    def setConfiguration(self,confDict):
        return self.radioObj.setConfiguration(confDict)
    