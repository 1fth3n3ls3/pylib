from PySide2 import QtWidgets, QtCore, QtGui

class ConverterWindow(QtWidgets.QMainWindow):
    converPressed = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(ConverterWindow, self).__init__(parent)
        


def createWindow():
    window =  ConverterWindow()
    window.setWindowTitle('Hierarchy Converter')

    container = QtWidgets.QWidget(window)

    

    layout = QtWidgets.QHBoxLayout(container)
    container.setLayout(layout)
    label = QtWidgets.QLabel('Prefix: ', container)
    textBox = QtWidgets.QLineEdit(container)
    button = QtWidgets.QPushButton('Convert', container)
    layout.addWidget(label)
    layout.addWidget(textBox)
    layout.addWidget(button)
    window.setCentralWidget(container)

    def onClick():
        window.converPressed.emit(textBox.tex())
    
    button.clicked.connect(onClick)

    return window
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = createWindow()

    win.show()

    app.exec_()