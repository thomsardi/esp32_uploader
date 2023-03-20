import pyqt5ac
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
pathList = []
addPath = os.getcwd() + "\\resources"
# print(addPath)
sys.path.append(addPath)

# print(sys.path)

from resources.ui_files.definition import UI_FILE_DIR
from resources.ui_py.definition import UI_PY_DIR
from resources.assets.definition import RESOURCE_DIR

def convertUi() :
    ioPaths = [
        [UI_FILE_DIR+"/*.ui", UI_PY_DIR+"/%%FILENAME%%_ui.py"],
        [RESOURCE_DIR+"/*.qrc", addPath+"/%%FILENAME%%_rc.py"]
    ]
    pyqt5ac.main(ioPaths=ioPaths)

convertUi()

from resources.ui_py.MainWindow_ui import Ui_MainWindow

class MainScreen(QtWidgets.QMainWindow) :
    def __init__(self, *args, **kwargs) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

if __name__ == '__main__' :
    app = QtWidgets.QApplication([])
    widget = MainScreen()
    widget.show()
    app.exec_()