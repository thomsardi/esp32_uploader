import pyqt5ac
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from resources.ui_files.definition import UI_FILE_DIR
from resources.ui_py.definition import UI_PY_DIR
from resources.assets.definition import RESOURCE_DIR

# print(addPath)
sys.path.append(RESOURCE_DIR)

def convertUi() :
    ioPaths = [
        [UI_FILE_DIR+"/*.ui", UI_PY_DIR+"/%%FILENAME%%_ui.py"],
        [RESOURCE_DIR+"/*.qrc", RESOURCE_DIR+"/%%FILENAME%%_rc.py"]
    ]
    pyqt5ac.main(ioPaths=ioPaths)

convertUi()

from resources.ui_py.MainWindow_ui import Ui_MainWindow
from resources.modules.SerialUsbFinder import SerialUsbFinder
from resources.modules.EspUploader import EspUploader

class MainScreen(QtWidgets.QMainWindow) :
    def __init__(self, *args, **kwargs) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.serialUsbFinder = SerialUsbFinder()
        self.ui.setupUi(self)
        self.ui.uploadBtn.clicked.connect(self.uploadClicked)
        self.ui.portComboBox.currentIndexChanged.connect(self.portComboIndexChanged)
        
    def uploadClicked(self) :
        bootloaderPath = self.ui.bootloaderLineEdit.text()
        partitionPath = self.ui.partitionLineEdit.text()
        firmwarePath = self.ui.firmwareLineEdit.text()
        filesystemPath = self.ui.filesystemlineEdit.text()
        isSingleMethod = self.ui.methodComboBox.currentIndex()
        if (bootloaderPath == "") :
            self.showMessageBox("Please fill the bootloader binary file")
            return
        if (partitionPath == "") :
            self.showMessageBox("Please fill the partition binary file")
            return
        if (firmwarePath == "") :
            self.showMessageBox("Please fill the firmware binary file")
            return
        
        if (isSingleMethod) :
            port = self.ui.portComboBox.currentText()
            espUploader = EspUploader()
            espUploader.bootloaderPath = bootloaderPath
            espUploader.partitionPath = partitionPath
            espUploader.firmwarePath = firmwarePath
            espUploader.port = port
            espUploader.start()
        
    def showMessageBox(self, description : str) :
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(description)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec()
        

if __name__ == '__main__' :
    app = QtWidgets.QApplication([])
    widget = MainScreen()
    widget.show()
    app.exec_()