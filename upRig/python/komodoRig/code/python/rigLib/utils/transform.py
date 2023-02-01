""""
transform @ utils

Function to manipulate and create transform
"""

import maya.cmds as mc

from . import name

def makeOffsetGrp (object, prefix = ''):

    """
    make offset group for given object

    @param object: transform object to offset group
    @param prefix:str, prefix to name new objects
    @param return:str, name of new offset group
    """

    if not prefix:

        prefix = name.removeSuffix(object)

    offsetGrp = mc.group(n= prefix + "Offset_GRP", em=1)

    objectParents = mc.listRelatives(object, p=1)

    if objectParents:

        mc.parent(offsetGrp, objectParents[0])

    #match object transforms
    mc.delete(mc.parentConstraint(object, offsetGrp))
    mc.delete(mc.scaleConstraint(object, offsetGrp))

    # parent object under offset group

    mc.parent (object, offsetGrp)

    return offsetGrp
