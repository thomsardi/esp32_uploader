from PyQt5 import QtCore
import threading
import esptool
import csv

class EspUploader(threading.Thread, QtCore.QObject) :
    isDone = QtCore.pyqtSignal(str, int)
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        # super().__init__()
        self.daemon = True
        self.__port = ""
        self.__baudRate = 460800
        self.__chip = "esp32"

        # self.__bootloaderPath = "bin/bootloader.bin"
        self.__bootAppPath = "bin/boot_app0.bin"
        self.__partitionPath = "bin/partition"
        self.__firmwarePath = ""
        self.__systemPath = ""
        
        self.__bootloaderAddress = "0x1000"
        self.__partitionAddress = "0x8000"
        self.__bootAppAddress = "0xe000"
        self.__firmwareAddress = "0x10000"
        self.__systemAddress = "0x290000"
        self.__partition = "4MB"

        self.__flashMode = "dio"

    def run(self) :
        firmwarePath = self.__firmwarePath
        systemPath = self.__systemPath
        bootLoaderPath = self.__bootloaderPath
        bootAppPath = self.__bootAppPath
        partitionPath = self.__partitionPath
        portName = self.__port
        # header = []
        # if(self.__partition == "8MB") :
        #     file = open("resources/partition-tables/default_8MB.csv")
        #     partitionPath = self.__partitionPath.replace("partition", "partition_8MB.bin") 
        # elif(self.__partition == "16MB") :
        #     file = open("resources/partition-tables/default_16MB.csv")
        #     partitionPath = self.__partitionPath.replace("partition", "partition_16MB.bin") 
        # else :
        #     file = open("resources/partition-tables/default.csv")
        #     partitionPath = self.__partitionPath.replace("partition", "partition_4MB.bin") 
        # csvreader = csv.reader(file)
        # header = next(csvreader)
        # rows = []
        # for row in csvreader :
        #     if(row[0] == "app0") :
        #         self.__firmwareAddress = row[3]
        #     elif(row[0] == "spiffs") :
        #         self.__systemAddress = row[3]
        #     elif(row[0] == "otadata") :
        #         self.__bootAppAddress = row[3]
        #     rows.append(row)
        
        command = []
        command.extend(["--chip", self.__chip, "--before", "default_reset", "--after", "hard_reset"])
        command.append("--port")
        command.append(portName)
        command.append("--baud")
        command.append(str(self.__baudRate))
        command.extend(["write_flash", "-z", "--flash_mode", self.__flashMode, "--flash_freq", "40m", "--flash_size", self.__partition])
        command.extend([self.__bootloaderAddress, bootLoaderPath, self.__partitionAddress, partitionPath, self.__bootAppAddress, bootAppPath])

        if(self.__bootloaderPath == "") : #if no bootloader, then return
            self.isDone.emit(portName, 0)
            return
        if(self.__partitionPath == "") :
            self.isDone.emit(portName, 0)
            return

        if (firmwarePath != "" and systemPath != "") : #if both firmware and filesystem address not ""
            command.extend([self.__firmwareAddress, firmwarePath, self.__systemAddress, systemPath])
            commandToSend = ' '.join(command)
        elif (firmwarePath != "") : #if firmware address is not ""
            command.extend([self.__firmwareAddress, firmwarePath])
            commandToSend = ' '.join(command)
        elif (systemPath != "") : #if filesystem address is not ""
            command.extend([self.__systemAddress, systemPath])
            commandToSend = ' '.join(command)

        print(commandToSend)
        try :
            # print(commandToSend)
            # esptool.main(command)
            self.isDone.emit(portName, 1)
        except :
            self.isDone.emit(portName, 0)

    @property
    def port(self) :
        return self.__port

    @port.setter
    def port(self, port) :
        self.__port = port
    
    @property
    def baudRate(self) :
        return self.__baudRate

    @baudRate.setter
    def baudRate(self, baudRate) :
        self.__baudRate = baudRate

    @property
    def chip(self) :
        return self.__chip
    @chip.setter
    def chip(self, chip) :
        self.__chip = chip
    
    @property
    def firmwarePath(self) :
        return self.__firmwareAddress

    @firmwarePath.setter
    def firmwarePath(self, firmwarePath) :
        self.__firmwarePath = firmwarePath
    
    @property
    def systemPath(self) :
        return self.__systemPath
    
    @systemPath.setter
    def systemPath(self, systemPath) :
        self.__systemPath = systemPath

    @property
    def partitionPath(self) :
        return self.__partitionPath

    @partitionPath.setter
    def partitionPath(self, partitionPath) :
        self.__partitionPath = partitionPath
    
    @property
    def bootloaderPath(self) :
        return self.__bootloaderPath
    
    @bootloaderPath.setter
    def bootloaderPath(self, bootloaderPath) :
        self.__bootloaderPath = bootloaderPath