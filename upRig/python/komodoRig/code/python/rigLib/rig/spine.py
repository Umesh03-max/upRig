"""
spine @ rig
"""

from xml.sax import make_parser
import maya.cmds as mc

from ..base import module
from ..base import control

def build(spineJoints, rootJnt, spineCurve, bodyLocator, pelvisLocator, chestLocator, prefix = 'spine', rigScale = 1.0, baseRig = None):

    """
    @param spineJoints:list (str), list for 6 spine joints
    @param rootJnt:str, root joint
    @param spineCurve:str, name of spine cubic curve with 5 CVs matching first 5 spine joints
    @param bodyLocator:str, refrence transform of body control
    @param pelvisLocator:str, refrence transform of pelvis control
    @param chestLocator:str, refrence transform of chest control
    @param prefix:str, prefix to name new objects
    @param rigScale:float, scale factor of size of controls
    @param baseRig: instance of base.module.Base controls
    @return: dictionary of rig module objects    
    """

    #make rig module

    rigModule = module.Module (prefix=prefix, baseObj=baseRig)

    #make spine curve clusters

    spineCurveCVs = mc.ls (spineCurve + '.cv[*]', fl =1 )
    numSpineCVs = len(spineCurveCVs)
    spineCurveClusters = []

    for i in range(spineCurveCVs):
        cls = mc.cluster(spineCurveCVs[i], n = prefix + 'Cluster%d' % (i + 1))[1]
        spineCurveClusters.append(cls)

    mc.hide (spineCurveClusters)

    #make controls

    bodyCtrl = control.Control (prefix = prefix + 'Body', translateTo= bodyLocator, scale = rigScale *4, parent= rigModule.controlsGrp)
    pelvisCtrl = control.Control (prefix = prefix + 'Body', translateTo= pelvisLocator, scale = rigScale *6, parent= bodyCtrl.C)
    chestCtrl = control.Control (prefix = prefix + 'Body', translateTo= chestLocator, scale = rigScale *6, parent= bodyCtrl.C)
    middleCtrl = control.Control (prefix = prefix + 'Body', translateTo= spineCurveClusters[2], scale = rigScale *6, parent= bodyCtrl.C)

    #attach controls

    mc.parentConstraint (chestCtrl.C, pelvisCtrl.C, middleCtrl.Off, sr= ['x', 'y', 'z'], mo =1)

    # attach clusters
    mc.parent (spineCurveClusters[3:], chestCtrl.C)
    mc.parent (spineCurveClusters[2], middleCtrl.C)
    mc.parent (spineCurveClusters[:2], pelvisCtrl.C)

    #make IK Handle 

    spineIK = mc.ikHandle (n = prefix + 'ikh', sol= 'ikSplineSolver', sj=spineJoints[0], ee= spineJoints [-2], c=spineCurve, ccv=0, parentCurve = 0)[0]

    mc.hide(spineIK)
    mc.parent (spineIK, rigModule.extraGrp)

    #setup IK Twist

    mc.setAttr (spineIK + '.dtce', 1)
    mc.setAttr (spineIK + '.dwut', 4)
    mc.connectAttr (chestCtrl.C + '.worldMatrix[0]', spineIK + '.dwue')
    mc.connectAttr (pelvisCtrl.C + '.worldMatrix[0]', spineIK + '.dwum')

    #attach root joint

    mc.parentConstraint (pelvisCtrl.C, rootJnt, mo=1)

    return {'module': rigModule}