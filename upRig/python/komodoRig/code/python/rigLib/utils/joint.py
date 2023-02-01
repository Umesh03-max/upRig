"""
joint utils @utils
"""

import maya.cmds as mc

def listHeirarchy(topJoint, withEndJoints = True):

    """
    list joint heirarchy starting with top joint

    @param topJoint: str, joint to get listed with its joint heirarchy
    @param withEndJoints: bool, list heirarchy including end joints
    @return: list (str), listed joints starting with top joint 
    """

    listedJoints = mc.listRelatives(topJoint, type = 'joint', ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()

    completeJoints =  listedJoints[:]

    if not withEndJoints:

        completeJoints = [j for j in listedJoints if mc.listRelatives(j, c=1, type='joint')]

    return completeJoints