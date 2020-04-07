import pymel.core as pmc
import utils

# Version 3

def safe_setparent(node, parent):
    """`node.setParent(parent)` if `parent` is
    not the same as `node`'s existing parent.
    """
    if node.getParent() != parent:
        node.setParent(parent)

GREEN = 14
BLUE = 6
YELLOW = 17

def _convert_to_joint(node, parent, prefix,
                      jnt_size, lcol, rcol, ccol):
    pmc.select(clear=True)
    j = pmc.joint(name=prefix + node.name())
    safe_setparent(j, parent)
    j.translate.set(node.translate.get())
    j.rotate.set(node.rotate.get())
    j.setRadius(jnt_size)
    def calc_wirecolor():
        x = j.translateX.get()
        if x < -0.001:
            return rcol
        elif x > 0.001:
            return lcol
        else:
            return ccol
    j.overrideColor.set(calc_wirecolor())
    return j

def convert_to_skeleton(rootnode,
                        prefix='skel_',
                        joint_size=1.0,
                        lcol=BLUE,
                        rcol=GREEN,
                        ccol=YELLOW,
                        _parent=None):

    if _parent is None:
        _parent = rootnode.getParent()
    j = _convert_to_joint(
        rootnode, _parent, prefix, joint_size, lcol, rcol, ccol)

    children = [node for node in rootnode.getChildren() if utils.isType(node, 'transform')]

    for c in children:
        convert_to_skeleton(c, prefix, joint_size, lcol, rcol, ccol, j)
    return j


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
    def handle_node(node): #(2)
        """If any of the ancestors of n are in realroots,
        just return, otherwise, append n to realroots.
        """
        for ancestor in ancestors(node):
            if ancestor in nodes: #(4)
                return
        result.append(node) #(5)
    for node in nodes: #(3)
        handle_node(node)
    return result