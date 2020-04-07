import pymel.core as pmc
import utils
import skeletonutils
reload(skeletonutils)

GREEN = 14
BLUE = 6
YELLOW = 17
PURPLE = 8
AQUA = 28

SETTINGS_DEFAULT = {
    'joint_size': 1.0,
    'right_color': BLUE,
    'left_color': GREEN,
    'center_color': YELLOW,
    'prefix': 'char_',
}
SETTINGS_GAME2 = {
    'joint_size': 25.0,
    'right_color': PURPLE,
    'left_color': AQUA,
    'center_color': GREEN,
    'prefix': 'game2char_',
}

#(2)
def convert_hierarchies_main(settings=SETTINGS_DEFAULT):
    nodes = pmc.selected(type='transform')
    if not nodes:
        pmc.warning('No transforms selected.')
        return
    new_roots = convert_hierarchies(nodes, settings)
    print('Created:', ','.join([r.name() for r in new_roots]))

#(2)
def convert_hierarchies(rootnodes, settings=SETTINGS_DEFAULT):
    roots = skeletonutils.uniqueroots(rootnodes)
    print('real roots:' + " ".join([node.name() for node in roots]))
    result = [convert_hierarchy(r, settings) for r in roots]
    return result

# (2)
def convert_hierarchy(rootnode,  settings=SETTINGS_DEFAULT):
    result = skeletonutils.convert_to_skeleton(rootnode,
                                               joint_size=settings['joint_size'],
                                               prefix=settings['prefix'],
                                               rcol=settings['right_color'],
                                               lcol=settings['left_color'],
                                               ccol=settings['center_color'])
    pmc.delete(rootnode)
    return result

if __name__ == "__main__":
    convert_hierarchies_main()