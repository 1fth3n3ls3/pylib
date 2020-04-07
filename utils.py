import pymel.core as pmc


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