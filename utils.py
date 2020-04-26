
import pymel.core as pmc
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtWidgets

import time

def getMayaWindow():
    winptr = omui.MQtUtil.mainWindow()
    if winptr is None:
        raise RuntimeError('No maya window found.')
    
    window = wrapInstance(long(winptr), QtWidgets.QWidget)
    

    return window





def firtsOrDefault(seq, predicate=None, default=None):
    for each in seq:
        if predicate is None or predicate(each):
            return each
    return default

def head(seq, count):
    lst = []
    for each in seq:
        if len(lst) == count:
            break 
        else: 
            lst.append(each) 
    return lst 

def tail(seq, count):
    lst = list(seq)
    return lst[-count:] 

def isExactType(node, typename):
    """node.type() == typename"""
    return node.type() == typename

def isType(node, typename):
    """Return True if node.type() is typename or
    any subclass of typename."""
    return typename in node.nodeType(inherited=True)

def ancestors(node):
    """Return a list of ancestors, starting with the direct parent
    and ending with the top-level (root) parent."""
    result = []
    parent = node.getParent()
    while parent is not None:
        result.append(parent)
        parent = parent.getParent()
    return result


def uniqueroots(nodes): #(1)
    """Returns a list of the nodes in `nodes` that are not
    children of any node in `nodes`."""
    result = []
    def handle_node(n): #(2)
        """If any of the ancestors of n are in realroots,
        just return, otherwise, append n to realroots.
        """
        for ancestor in ancestors(n):
            if ancestor in nodes: #(4)
                return
        result.append(n) #(5)
    for node in nodes: #(3)
        handle_node(node)
    return result

# context managers and decorators.

class undoChunk(object):
    '''Context manager'''
    def __enter__(self):
        pmc.undoInfo(openChunk=True)
    
    def __exit__(self, *exc_info):
        pmc.undoInfo(closeChunk=True)

def chunkUndo(func):
    def inner(*args, **kwargs):
       pmc.undoInfo(openChunk=True)
       try:
           return func(*args, **kwargs)
       except RuntimeError as ex:
           print(ex)
       finally:
           pmc.undoInfo(closeChunk=True)
    
    return inner

class undoOnError(object):
    def __enter__(self):
        pmc.undoInfo(openChunk=True)
    def __exit__(self, exc_type, exc_val, exc_tb):
        pmc.undoInfo(closeChunk=True)
        if exc_val is not None:
            pmc.undo()


class atTime(object):
    def __init__(self, t):
        self.t = t
        self.oldt = None
    def __enter__(self):
        self.oldt = pmc.getCurrentTime()
        pmc.setCurrentTime(self.t)
    def __exit__(self, *_):
        if self.oldt is not None:
            pmc.setCurrentTime(self.oldt)

class setFilePrompt(object):
    def __init__(self, value):
        self.value = value
        self.buffer = None

    def __enter__(self):
        self.buffer = cmds.file(query=True, prompt=True)
        cmds.file(prompt=self.value)

    def __exit__(self, *_):
        cmds.file(prompt=self.buffer)

class AnimationLayers(object):  
    def __init__(self, *layers):
        self.layers = layers
        self.bufferLayers = None

    def __enter__(self):
        self.bufferLayers = self._getActiveLayers()

        for each in self._getAnimLayers():
            if each.name() not in self.layers:
                pmc.mel.eval('animLayerMuteCallBack "{0}" "1";'.format(each.name()))
                pmc.animLayer(each, edit=True, mute=True, lock=True)
            else:
                pmc.mel.eval('animLayerMuteCallBack "{0}" "1";'.format(each.name()))
                pmc.animLayer(each, edit=True, mute=False, lock=False)
        
        pmc.mel.eval('updateEditorFeedbackAnimLayers("AnimLayerTab")')

    def __exit__(self, *_):
        if self.bufferLayers:
            for each in self._getAnimLayers():
                if each in self.bufferLayers:
                    pmc.mel.eval('animLayerMuteCallBack "{0}" "1";'.format(each.name()))
                    pmc.animLayer(each.name(), edit=True, lock=True)
                    pmc.animLayer(each.name(), edit=True, mute=True)
                else:
                    pmc.mel.eval('animLayerMuteCallBack "{0}" "1";'.format(each.name()))
                    pmc.animLayer(each.name(), edit=True, lock=False)
                    pmc.animLayer(each.name(), edit=True, mute=False)
            pmc.mel.eval('updateEditorFeedbackAnimLayers("AnimLayerTab")')
            
            print(_)

    def _getActiveLayers(self):
        animLayers = self._getAnimLayers()
        return [layer for layer in animLayers if not self._isMuted(layer)]

    def _getAnimLayers(self, predicate=None):
        baseAnimLayer = self._getBaseAnimLayer()
        animLayers = []
        if baseAnimLayer:
            animLayers.append(baseAnimLayer)
            childrenLayers = pmc.animLayer(baseAnimLayer, query=True, children=True)
            animLayers.extend(childrenLayers)
        
        return animLayers


    def _getBaseAnimLayer(self):
        return pmc.animLayer(query=True, root=True)

    def _isMuted(self, layer):
        return pmc.animLayer(layer, query=True, mute=True)

    
def readDuration(func):
    def inner(*args, **kwargs):
        startTime = time.clock()
        result = func(*args, **kwargs)
        endTime = time.clock()
        print('{0} took {1} in execution'.format(func.__name__, (endTime-startTime)))
        
        return result
    
    return inner
    
