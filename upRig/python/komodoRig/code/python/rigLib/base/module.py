""""
module for making rig structure and rig build
"""

#from enum import _EnumNames
import maya.cmds as mc

sceneObjectType = "rig"

from . import control

class Base():

    """"
    class for building top rig structure
    """

    def __init__(self, characterName = "new", scale = 1.0, mainCtrlAttachObj = ''):

        """
        @param characterName:str, character Name
        @param scale:float, scale of the character
        @return: None
        """

        self.topGrp = mc.group(n = characterName + 'rig_GRP', em=1)
        self.rigGrp = mc.group(n = 'rig_GRP', em=1, p= self.topGrp)
        self.modelGrp = mc.group(n = 'model_GRP', em=1, p= self.topGrp)

        characterNameAt = 'characterName'
        sceneObjectTypeAt =  'sceneObjectType'

        for at in [characterNameAt, sceneObjectTypeAt]:

            mc.addAttr(self.topGrp, longName = at, dt = "string")

        mc.setAttr(self.topGrp + '.' + characterNameAt, characterName, type = 'string', l = 1)
        mc.setAttr(self.topGrp + '.' + sceneObjectTypeAt, sceneObjectType, type = 'string', l = 1)


        ###global control
        global1Ctrl = control.Control(prefix = 'global1', scale = scale * 20, parent = self.rigGrp, lockChannels = ['v'])
        global2Ctrl = control.Control(prefix = 'global2', scale = scale * 18, parent = global1Ctrl.C, lockChannels = ['s', 'v'])

        self._flattenGlobalCtrlShape (global1Ctrl.C)
        self._flattenGlobalCtrlShape (global2Ctrl.C)


        for axis in ['y', 'z']:
            mc.connectAttr(global1Ctrl.C + '.sx', global1Ctrl.C + '.s' + axis)
            mc.setAttr(global1Ctrl.C + '.s' + axis, k = 0)

        ##make more groups

        self.jointsGrp = mc.group(n = 'joints_GRP', em=1, p= global2Ctrl.C)
        self.modulesGrp = mc.group(n = 'modules_GRP', em=1, p= global2Ctrl.C)

        self.extraGrp = mc.group(n = 'extra_GRP', em=1, p= self.rigGrp)
        mc.setAttr(self.extraGrp + '.it', 0, l = 1)

        mainCtrl = control.Control(prefix = 'main', scale = scale * 1, parent = global2Ctrl.C, translateTo = mainCtrlAttachObj, lockChannels = ['t', 'r', 's', 'v'])

        self._adjustMainCtrlShape ( mainCtrl, scale)

        if mc.objExists (mainCtrlAttachObj):
            
            mc.parentConstraint (mainCtrlAttachObj, mainCtrl.Off, mo= 1)

        mainVisAts = ['modelVis', 'jointsVis']
        mainDispAts = ['modelDisp', 'jointsDisp']
        mainObjList = [self.modelGrp, self.jointsGrp]
        mainObjDvList = [0, 1]

        # add visiblity connection

        for at , obj, dfVal in zip (mainDispAts, mainObjList, mainObjDvList):

            mc.addAttr(mainCtrl.C, ln = at, at = 'enum', enumName = 'normal:template:reference', k =1, dv = 2)
            mc.setAttr (mainCtrl.C + '.' + at, cb = 1)
            mc.setAttr (obj + '.ove', 1)
            mc.connectAttr (mainCtrl.C + '.' + at, obj + '.ovdt')

        # add model display connection
        
        for at , obj in zip (mainVisAts, mainObjList):

            mc.addAttr(mainCtrl.C, ln = at, at = 'enum', enumName = 'off:on', k =1, dv = dfVal)
            mc.setAttr (mainCtrl.C + '.' + at, cb = 1)
            mc.connectAttr (mainCtrl.C + '.' + at, obj + '.v')

    def _adjustMainCtrlShape (self, ctrl, scale):
        
        # adjust shape of main ctrl
        ctrlShapes = mc.listRelatives (ctrl.C, s=1, type = 'nurbsCurve')
        cls = mc.cluster(ctrlShapes) [1]
        mc.setAttr (cls +  '.ry', 90)
        mc.delete (ctrlShapes, ch=1)

        mc.move (5 * scale, ctrl.Off, moveY = True, relative = True)

    def _flattenGlobalCtrlShape(self, ctrlObject):

        #flatten Control Object Shapes
        ctrlShapes = mc.listRelatives (ctrlObject, s=1, type = 'nurbsCurve')
        cls = mc.cluster(ctrlShapes) [1]
        mc.setAttr (cls +  '.rz', 90)
        mc.delete (ctrlShapes, ch=1)

class Module():

    """"
    class for building module rig structure
    """

    def __init__(self, prefix = "new", baseObj = None ):

        """
        @param prefix:str, prefix to name new objects
        @param baseObj:instance of base.module.Base class
        @return: None
        """
        self.topGrp = mc.group(n = prefix + 'Module_GRP', em=1)

        self.controlsGrp = mc.group(n = prefix + 'Controls_GRP', em=1,p = self.topGrp)
        self.jointsGrp = mc.group(n = prefix + 'Joints_GRP', em=1,p = self.topGrp)
        self.partsGrp = mc.group(n = prefix + 'Parts_GRP', em=1,p = self.topGrp)
        self.extraGrp = mc.group(n = prefix + 'Extra_GRP', em=1,p = self.topGrp)

        mc.setAttr (self.extraGrp +  '.it', 0, l = 1)

        #parent Module

        if baseObj:
            mc.parent (self.topGrp, baseObj.modulesGrp)

