from PySide2 import QtWidgets, QtCore, QtGui

class Window(QtWidgets.QMainWindow):
    convertPressed = QtCore.Signal(str)
    
    def __init__(self, title='', parent=None):
        super(Window, self).__init__(parent=parent)
        self.setWindowTitle(title)
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
        # self.controller.selectionChanged.connect(self.updateStatusBar)

    def updateStatusBar(self, newSel):
        if not newSel:
            txt = 'Nothing selected.'
        elif len(newSel) == 1:
            txt = '{0} selected'.format(newSel[0])
        else:
            txt = '{0} objects selected.'.format(str(len(newSel)))
        self.statusBar().showMessage(txt)

    # events
    def onClick(self):
        self.convertPressed.emit(self.textBox.text())
    
class ConvertHierarchyController(QtCore.QObject):
    selectionChanged = QtCore.Signal(list)

def _pytest():
    import random

    controller = ConvertHierarchyController()

    def nextSel():
        return random.choice([
                                [],
                                ['single'],
                                ['single', 'double']])
    
    def onConvert(prefix):
        print('Convert clicked! Prefix:', prefix)
        controller.selectionChanged.emit(nextSel())

    app = QtWidgets.QApplication([])
    win = Window('Hierarchy Converter')
    win.convertPressed.connect(onConvert)
    controller.selectionChanged.connect(win.updateStatusBar)
    win.show()

    app.exec_()

if __name__ == "__main__":

    _pytest()
