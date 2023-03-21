import pyqt5ac
import sys
import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from resources.ui_files.definition import UI_FILE_DIR
from resources.ui_py.definition import UI_PY_DIR
from resources.assets.definition import ASSET_DIR
from resources.bin_files.definition import BIN_DIR

# print(addPath)
sys.path.append(ASSET_DIR)

def convertUi() :
    ioPaths = [
        [UI_FILE_DIR+"/*.ui", UI_PY_DIR+"/%%FILENAME%%_ui.py"],
        [ASSET_DIR+"/*.qrc", ASSET_DIR+"/%%FILENAME%%_rc.py"]
    ]
    pyqt5ac.main(ioPaths=ioPaths)

convertUi()

from resources.ui_py.MainWindow_ui import Ui_MainWindow
from resources.modules.SerialUsbFinder import SerialUsbFinder
from resources.modules.EspUploader import EspUploader
from resources.modules.OutputWindow import OutputWindow

class MainScreen(QtWidgets.QMainWindow) :
    def __init__(self, *args, **kwargs) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serialUsbFinder = SerialUsbFinder()
        self.ui.uploadBtn.clicked.connect(self.uploadClicked)
        self.ui.methodComboBox.currentIndexChanged.connect(self.methodComboBoxIndexChanged)
        self.ui.refreshBtn.clicked.connect(self.refreshButtonClicked)
        self.ui.clearBtn.clicked.connect(self.clearTerminalLineEdit)
        self.ui.bootloaderBrowseBtn.clicked.connect(self.bootloaderBrowseBtnClicked)
        self.ui.partitionBrowseBtn.clicked.connect(self.partitionBrowseBtnClicked)
        self.ui.firmwareBrowseBtn.clicked.connect(self.firmwareBrowseBtnClicked)
        self.ui.filesystemBrowseBtn.clicked.connect(self.filesystemBrowseBtnClicked)
        palette = self.ui.terminalPlainText.viewport().palette()
        palette.setColor(self.ui.terminalPlainText.viewport().backgroundRole(), QtGui.QColor(0,0,0))
        self.ui.terminalPlainText.setPalette(palette)
        self.__totalUpload = 0
        self.__successUpload = 0
        self.__failedUpload = 0
        self.isSingleMethod = False
        self.portNameList = []
        self.ui.portComboBox.clear()
        portList = []
        for port in self.serialUsbFinder.ports :
            portList.append(port.name)
        self.ui.portComboBox.addItems(portList)
        if (self.ui.methodComboBox.currentIndex() <= 0) :
            self.ui.portComboBox.setDisabled(True)
        else :
            self.ui.portComboBox.setEnabled(True)
        
    def uploadClicked(self) :
        bootloaderPath = self.ui.bootloaderLineEdit.text()
        partitionPath = self.ui.partitionLineEdit.text()
        firmwarePath = self.ui.firmwareLineEdit.text()
        filesystemPath = self.ui.filesystemLineEdit.text()
        self.isSingleMethod = self.ui.methodComboBox.currentIndex()
        if (bootloaderPath == "") :
            self.showMessageBox("Please fill the bootloader binary file")
            return
        if (partitionPath == "") :
            self.showMessageBox("Please fill the partition binary file")
            return
        if (firmwarePath == "") :
            self.showMessageBox("Please fill the firmware binary file")
            return
        
        sys.stdout = OutputWindow()
        sys.stdout.isDataAvailable.connect(self.updateTerminalPlainText)

        if (self.isSingleMethod) :
            port = self.ui.portComboBox.currentText()
            espUploader = EspUploader()
            espUploader.bootloaderPath = bootloaderPath
            espUploader.partitionPath = partitionPath
            espUploader.firmwarePath = firmwarePath
            espUploader.port = port
            espUploader.isDone.connect(self.uploadDone)
            espUploader.start()
        else :
            usbList = self.serialUsbFinder.getUsbDevice()
            for usb in usbList :
                espUploader = EspUploader()
                espUploader.bootloaderPath = bootloaderPath
                espUploader.partitionPath = partitionPath
                espUploader.firmwarePath = firmwarePath
                espUploader.port = usb.name
                espUploader.isDone.connect(self.uploadDone)
                espUploader.start()
    
    def refreshButtonClicked(self) :
        self.serialUsbFinder.scanPort()
        self.ui.portComboBox.clear()
        portList = []
        for port in self.serialUsbFinder.ports :
            portList.append(port.name)
        self.ui.portComboBox.addItems(portList)

    def bootloaderBrowseBtnClicked(self) :
        dir = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Firmware File', BIN_DIR , 'bin file (*.bin)')
        self.ui.bootloaderLineEdit.setText(dir[0])
    
    def partitionBrowseBtnClicked(self) :
        dir = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Firmware File', BIN_DIR , 'bin file (*.bin)')
        self.ui.partitionLineEdit.setText(dir[0])
    
    def firmwareBrowseBtnClicked(self) :
        dir = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Firmware File', BIN_DIR , 'bin file (*.bin)')
        self.ui.firmwareLineEdit.setText(dir[0])
    
    def filesystemBrowseBtnClicked(self) :
        dir = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Firmware File', BIN_DIR , 'bin file (*.bin)')
        self.ui.filesystemLineEdit.setText(dir[0])
    
    def methodComboBoxIndexChanged(self) :
        print("method index changed")
        index = self.ui.methodComboBox.currentIndex()
        if (index <= 0) :
            self.ui.portComboBox.setDisabled(True)
        else :
            self.ui.portComboBox.setEnabled(True)

        self.ui.portComboBox.clear()
        portList = []
        for port in self.serialUsbFinder.ports :
            portList.append(port.name)
        self.ui.portComboBox.addItems(portList)

    def clearTerminalLineEdit(self) :
        self.ui.terminalPlainText.clear()
        self.updateCursorPos()

    def updateTerminalPlainText(self, data) :
        self.updateCursorPos()
        text = data
        self.ui.terminalPlainText.insertPlainText(text)
    
    def updateCursorPos(self) :
        plainTextCursor = QtGui.QTextCursor()
        plainTextCursor = self.ui.terminalPlainText.textCursor()
        self.ui.terminalPlainText.moveCursor(plainTextCursor.MoveOperation.End, plainTextCursor.MoveMode.MoveAnchor)

    def uploadDone(self, portName, status) :
        if(self.isSingleMethod) :
            numOfUsb = 1
        else :    
            numOfUsb = len(self.serialUsbFinder.getUsbDevice())
        
        self.__totalUpload += 1
        if (status) :
            self.__successUpload += 1
            statusText = "Success"
        else :
            self.__failedUpload += 1
            statusText = "Error"
        portNameStatus = "%s : %s" %(portName, statusText)
        print("Port : ", portName)
        print("Upload Status : ", statusText)
        self.portNameList.append(portNameStatus)
        if(self.__totalUpload >= numOfUsb) :
            sys.stdout = sys.__stdout__
            message = []
            message.append("Finish Upload into : %d device(s)" %(numOfUsb))
            message.append("Success Upload : %d device(s)" %(self.__successUpload))
            message.append("Failed Upload : %d device(s)" %(self.__failedUpload))
            description = "\n".join(message)
            detailMessage = []
            detailMessage.append("Detail port list : ")
            portNameList = "\n".join(self.portNameList)
            detailMessage.append(portNameList)
            detail = "\n".join(detailMessage)
            self.showMessageBoxOnUploadDone(description, detail)
            self.__totalUpload = 0
            self.__successUpload = 0
            self.__failedUpload = 0
            self.portNameList.clear()

    def showMessageBox(self, description : str, detail : str = "") :
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(description)
        if (detail != "") :
            msg.setDetailedText(detail)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec()

    def showMessageBoxOnUploadDone(self, description : str, detail : str = "") :
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Upload Report")
        msg.setText(description)
        if (detail != "") :
            msg.setDetailedText(detail)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec()    

if __name__ == '__main__' :
    app = QtWidgets.QApplication([])
    widget = MainScreen()
    widget.show()
    app.exec_()