"""
komodo dragon rig setup
main rig
"""

from rigLib.base import control
from rigLib.base import module
from rigLib.rig import spine

from . import komodo_deform
from . import project

import maya.cmds as mc

sceneScale = project.sceneScale

mainProjectPath = project.mainProjectPath

modelFilePath = '%s/%s/model/%s_model.mb'
builderSceneFilePath = '%s/%s/builder/%s_builder.mb' 

rootJnt = 'root1_jnt'
headJnt = 'head1_jnt'

def build(characterName):
    """
    main functions to build character rig
    """

    # new scene
    mc.file( new = True, f = True)

    # import buildScene
    builderFile = builderSceneFilePath % (mainProjectPath, characterName, characterName)
    mc.file (builderFile, i =1 )
    
    # make base
    baseRig = module.Base (characterName=characterName, scale = sceneScale, mainCtrlAttachObj = headJnt)

    # import model
    modelFile = modelFilePath % (mainProjectPath, characterName, characterName)
    mc.file (modelFile, i =1 )

    # parent model 
    modelGrp = '%s_model_grp' % characterName
    mc.parent (modelGrp, baseRig.modelGrp)

    # parent skeleton
    mc.parent(rootJnt, baseRig.jointsGrp) 

    # deform setup
    komodo_deform.build(baseRig, characterName) 

    # control setup
    makeControlSetup(baseRig)

def makeControlSetup(baseRig):
    """
    make control setup
    """

    #spine

    spineJoints = ['spine1_jnt', 'spine2_jnt', 'spine3_jnt', 'spine4_jnt', 'spine5_jnt', 'spine6_jnt']
    spineRig = spine.build(spineJoints = spineJoints, rootJnt = rootJnt, spineCurve= 'spine_crv', bodyLocator= 'body_loc', pelvisLocator = 'pelvis_loc', chestLocator= 'chest_loc', prefix = 'spine', rigScale = sceneScale, baseRig = baseRig)