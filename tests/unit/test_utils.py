import pylib
import maya.cmds as cmds
reload(pylib)
from pylib import utils
import pymel.core as pmc
import unittest
try:
    from mock import Mock
except: pass

class TestTail(unittest.TestCase):
    def test_list_provided_return_last_elements_requested(self):
        lst = [1, 2, 3]
        self.assertItemsEqual([3], utils.tail(lst, 1))

    def test_list_provided_return_none(self):
        lst = []
        self.assertItemsEqual([], utils.tail(lst, 2))
        
class TestHead(unittest.TestCase):
    def test_list_provided_return_last_elements_requested(self):
        lst = [1, 2, 3]
        self.assertItemsEqual([1], utils.head(lst, 1))

    def test_list_provided_return_none(self):
        lst = []
        self.assertItemsEqual([], utils.head(lst, 2))

class TestUndoChunk(unittest.TestCase):
    def setUp(self):
        for m in pmc.ls(type='joint'):
            if pmc.objExists(m):
                pmc.delete(m)

    def testUndoChunk(self):
        with utils.undoChunk():
            pmc.joint(), pmc.joint()
        self.assertEqual(len(pmc.ls(type='joint')), 2)
        pmc.undo()
        self.assertFalse(pmc.ls(type='joint'))

    def testChunkUndo(self):
        @utils.chunkUndo
        def spam():
            pmc.joint(), pmc.joint()
        spam()
        self.assertEqual(len(pmc.ls(type='joint')), 2)
        pmc.undo()
        self.assertFalse(pmc.ls(type='joint'))

class TestAtTime(unittest.TestCase):
    def testAtTime(self):
        pmc.setCurrentTime(1)
        with utils.atTime(2):
            print(type(pmc.getCurrentTime()))
            self.assertEqual(pmc.getCurrentTime(), 2)
        self.assertEqual(pmc.getCurrentTime(), 1)

class TestUndoOnError(unittest.TestCase):
    def testUndoOnError(self):
        def doit():
            with utils.undoOnError():
                pmc.joint()
                raise NotImplementedError()
        self.assertRaises(NotImplementedError, doit)
        self.assertFalse(pmc.ls(type='joint'))

class testSetFilePrompt(unittest.TestCase):
    def test_SetFilePrompt_return_False(self):
        cmds.file(prompt=False)
        with utils.setFilePrompt(True):
            self.assertTrue(cmds.file(q=True, prompt=True))
        self.assertFalse(cmds.file(q=True, prompt=True))

if __name__ == "__main__":
    unittest.main(exit=False)
