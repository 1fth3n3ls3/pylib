from PySide2 import QtWidgets, QtCore, QtGui

class Window(QtWidgets.QMainWindow):
    convertPressed = QtCore.Signal(str)
    
    def __init__(self, title=None, parent=None):
        super(Window, self).__init__(parent=parent)
        
        self.configureWidgets()
        self.connectEvents()

    def configureWidgets(self):
        self.container = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QHBoxLayout(self.container)
        self.container.setLayout(self.layout)
        self.label = QtWidgets.QLabel('Prefix: ', self.container)
        self.textBox = QtWidgets.QLineEdit(self.container)
        self.button = QtWidgets.QPushButton('Convert', self.container)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textBox)
        self.layout.addWidget(self.button)
        self.setCentralWidget(self.container)

    def connectEvents(self):
        self.button.clicked.connect(self.onClick)

    # events
    def onClick(self):
        self.convertPressed.emit(self.textBox.text())
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Window('Hierarchy Converter')

    def onConvert(prefix):
        print('Convert clicked! Prefix:', prefix)

    win.convertPressed.connect(onConvert)
    win.show()

    app.exec_()