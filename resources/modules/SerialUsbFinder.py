from serial.tools import list_ports
import typing
from serial.tools.list_ports_common import ListPortInfo

class SerialUsbFinder():
    def __init__(self) :
        super().__init__()
        self.__ports = list_ports.comports()
            
    def scanPort(self):
        self.__ports = list_ports.comports() 

    def getUsbDevice(self) -> typing.List[ListPortInfo] :
        self.__ports = list_ports.comports()
        usbList = []
        for p in self.__ports :
            desc = p.description.lower()
            if "usb" in desc :
                usbList.append(p)
        return usbList
    
    @property
    def ports(self) :
        return self.__ports