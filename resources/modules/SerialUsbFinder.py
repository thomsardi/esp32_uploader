from serial.tools import list_ports

class SerialUsbFinder():
    def __init__(self) :
        super().__init__()
        self.__ports = list_ports.comports()
            
    def scanPort(self):
        self.__ports = list_ports.comports() 

    def getUsbDevice(self) :
        usbList = []
        for p in self.__ports :
            desc = p.description.lower()
            if "usb" in desc :
                usbList.append(p)
        return usbList