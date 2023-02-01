"""
komodo dragon rig setup
deformation setup
"""

import maya.cmds as mc
import maya.mel as mm

import os
from rigLib import base
from rigTools import bSkinSaver

from rigLib.utils import name
from rigLib.base import module

from . import project

skinWeightsDir = 'weights/skincluster'
swExt = '.swt'

bodyGeo = 'body_geo'
bodyMidResGeo = 'body_midres_geo'

def build(baseRig, characterName):

    modelGrp = '%s_model_grp' % characterName

    # make twist joints
    refTwistJoints = ['l_elbow1_jnt', 'l_knee1_jnt', 'r_elbow1_jnt', 'r_knee1_jnt']
    makeTwistJoints (baseRig, refTwistJoints)

    # load skin weights
    geoList = _getModelGeoObjects (modelGrp)
    loadSkinWeights (characterName, geoList)

    # apply mush deformer
    _applyDeltaMush (bodyMidResGeo)

    # wrap hiRes body mesh

    _makeWrap ([bodyGeo], bodyMidResGeo)

    pass
def _makeWrap (wrappedObjs, wrapperObjs):

    mc.select(wrappedObjs)
    mc.select (wrapperObjs, add = 1)
    mm.eval('deformer -type wrap body_geo')

def _applyDeltaMush (geo):

    deltaMushDf = mc.deltaMush(geo, smoothingIterations = 50)[0]


def _getModelGeoObjects (modelGrp):

    geoList = [mc.listRelatives(o, p=1) [0] for o in mc.listRelatives(modelGrp, ad= 1, type='mesh')]

    return

def makeTwistJoints (baseRig, parentJoints):

    twistJointsMainGrp = mc.group (n = 'twistJoints_GRP', p = baseRig.jointsGrp, em =1)

    for parentJoint in parentJoints:

        prefix = name.removeSuffix (parentJoint)
        prefix = prefix [:-1]
        parentJntChild = mc.listRelatives (parentJoint, c=1, type = 'joint')[0]

        # make twist joints

        twistJointsGrp = mc.group (n = prefix + 'TwistJoint_GRP', parent = twistJointsMainGrp, em =1)

        twistParentsJnt = mc.duplicate (parentJoint, n = prefix + 'twist1_jnt', parentOnly = True)[0]
        twistChildJnt = mc.duplicate (parentJntChild, n = prefix + 'twist2_jnt', parentOnly = True)[0]

        # adjust Twist Joints

        origJntradius = mc.getAttr (parentJoint + ".radius")

        for j in [twistParentsJnt, twistChildJnt]:

            mc.setAttr (j + '.radius', origJntradius * 2)
            mc.color (j, ud = 1)

        mc.parent(twistChildJnt, twistParentsJnt)
        mc.parent(twistParentsJnt, twistJointsGrp)

        # attach twist Joints
        mc.pointConstraint (parentJoint, twistParentsJnt)

        twistIK = mc.ikHandle(n = prefix + 'TwistJointIkh', sol = 'ikSCsolver', sj= twistParentsJnt, ee= twistChildJnt)[0]
        mc.hide (twistIK)
        mc.parent (twistIK, twistJointsGrp)
        mc.parentConstraint (parentJntChild, twistIK)



def saveSkinWeights(characterName, geoList = []):
    """
    save weights for geometry objects
    """

    for obj in geoList:
        # weight file
        wtFile = os.path.join (project.mainProjectPath, characterName, skinWeightsDir, obj + swExt)

        # save skin weight file
        mc.select (obj)
        bSkinSaver.bSaveSkinValues (wtFile)

def loadSkinWeights (characterName, geoList = []):
    """
    load weights for geometry objects
    """

    # saved weights path
    wtDir = os.path.join (project.mainProjectPath, characterName, skinWeightsDir)
    wtFiles = os.listdir( wtDir)

    # load skin weight file

    for wtFile in wtFiles:

        extRes = os.path.splitext(wtFile)

        # check extension 

        if not extRes > 1:

            continue

        # check skin weight file

        if not extRes[1] == swExt:
            
            continue

        if geoList and not extRes[0] in geoList:

            continue

        if not mc.objExists (extRes[0]):

            continue

        fullPathWtFile = os.path.join (wtDir, wtFile)
        bSkinSaver.bLoadSkinValues (loadOnSelection = False, inputFile = fullPathWtFile)

