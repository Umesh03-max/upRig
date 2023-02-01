""""
Control module for rig builder
"""

import maya.cmds as mc

class Control():

    """"
    class for building control
    """

    def __init__(self, prefix = 'new', scale = 1.0, translateTo = '', rotateTo = '', parent = '', shape = 'circle', lockChannels = ['s', 'v']):

        """
        @param prefix:str, prefix to name new controlShapes
        @param scale:float, scale value for the size of new control shapes
        @param translateTo:str, refrence objects for control position
        @param rotateTo:str, refrence objects for control orienation
        @param parent:str, object to be parent of new control
        @param lockChannels:list(str), list of channels on controls to be locked and non keyable

        @return: None
        """

        ctrlObject = mc.circle(n = prefix + "_CTRL", ch = 0, normal = [1,0,0], radius=scale)[0]
        ctrlOffset = mc.group(n = prefix + "Offset_GRP", em = 1 )
        mc.parent (ctrlObject, ctrlOffset)

        #color control
        ctrlShapes = mc.listRelatives(ctrlObject, s=1)[0]
        mc.setAttr (ctrlShapes + '.overrideEnabled', 1)

        if prefix.startswith('l_'):
            mc.setAttr (ctrlShapes + '.overrideColor', 6)

        elif prefix.startswith('r_'):
            mc.setAttr (ctrlShapes + '.overrideColor', 13)

        else:
            mc.setAttr (ctrlShapes + '.overrideColor', 22)
        
        ###translate offset delete constrains
        if mc.objExists (translateTo):
            mc.delete(mc.pointConstraint(translateTo, ctrlOffset))

        ###rotate offset delete constrains
        if mc.objExists ( rotateTo):
            mc.delete(mc.orientConstraint(rotateTo, ctrlOffset))

        ###parent offset delete constrains
        if mc.objExists ( parent):
            mc.parent(ctrlOffset, parent)

        ###lockChannels

        singleAttributeLockList = []

        for lockChannel in lockChannels:

            if lockChannel in ['t', 'r', 's']:

                for axis in ['x', 'y', 'z']:

                    at = lockChannel + axis

                    singleAttributeLockList.append (at)

            else:
                singleAttributeLockList.append (lockChannel)


        for at in singleAttributeLockList:

            mc.setAttr(ctrlObject + '.' + at, l = 1, k = 0)


        ###public members
        self.C = ctrlObject
        self.Off = ctrlOffset



        