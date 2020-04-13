import hierarchyconvertergui as hierconvgui
import utils
import pymel.core as pmc
import maya.OpenMaya as om
import charcreator

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.ConvertHierarchyController()
        def emiSelChanged(_):
            """This methods emits a list of selected nodes"""
            cont.selectionChanged.emit(pmc.selected(type='transform'))
        
        om.MEventMessage.addEventCallback('SelectionChanged', emiSelChanged)
        parent = utils.getMayaWindow()
        _window = hierconvgui.Window(cont, parent=parent)
        def onConvert(prefix):
            settings = dict(charcreator.SETTINGS_DEFAULT, 
                            prefix=unicode(prefix))
            charcreator.convert_hierarchies_main(settings)
        _window.convertPressed.connect(onConvert)
    _window.show()