import PyQt5.QtCore as qtc

class OutputWindow(qtc.QObject) :
    isDataAvailable = qtc.pyqtSignal(str)
    def __init__(self) :
        super().__init__()

    def write(self, text) :
        self.isDataAvailable.emit(text)

    def flush(self):
        None

    def isatty(self):
        return True
        