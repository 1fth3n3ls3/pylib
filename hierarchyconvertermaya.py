import hierarchyconvertergui as gui
import utils
import pymel.core as pmc
import maya.OpenMaya as om
import charcreator
from PySide2 import QtCore

_window = None

# def show():
#     global _window
#     if _window is None:
#         cont = gui.ConvertHierarchyController()
#         def emiSelChanged(_):
#             """This methods emits a list of selected nodes"""
#             cont.selectionChanged.emit(pmc.selected(type='transform'))
        
#         om.MEventMessage.addEventCallback('SelectionChanged', emiSelChanged)
#         parent = utils.getMayaWindow()
#         _window = gui.Window(cont, parent=parent)
#         def onConvert(prefix):
#             settings = dict(charcreator.SETTINGS_DEFAULT, 
#                             prefix=unicode(prefix))
#             charcreator.convert_hierarchies_main(settings)
#         _window.convertPressed.connect(onConvert)
#     _window.show()


class MayaController(QtCore.QObject):
    """
    # Call this way from shelve

    from pylib.hierarchyconvertermaya import MayaController
    MayaController()
    """
    view = None
    selectionChanged = QtCore.Signal(list) # must be defined as class atributte

    def __init__(self):
        super(MayaController, self).__init__() # needed to initialize QObject
        if MayaController.view is None:
            MayaController.view = gui.Window('Hierarchy Converter', parent=utils.getMayaWindow())
        self.establishConnections()
        MayaController.view.show()

    def emitSelectionChanged(self, _):
        """This methods emits a list of selected nodes"""
        self.selectionChanged.emit(pmc.selected(type='transform'))

    def establishConnections(self):
        self.selectionChanged.connect(MayaController.view.updateStatusBar)
        MayaController.view.convertPressed.connect(self.onConvert)
        om.MEventMessage.addEventCallback('SelectionChanged', self.emitSelectionChanged)

    def onConvert(self, prefix):
        settings = dict(charcreator.SETTINGS_DEFAULT, 
                        prefix=unicode(prefix))
        charcreator.convert_hierarchies_main(settings)


	

