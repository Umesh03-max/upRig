"""
upSnapper()
"""

import maya.cmds as mc 

def upSnapper(): #UI

    if mc.window('qSnap', exists = 1):
        mc.deleteUI('qSnap')

    mc.window('qSnap', title="up_Snapper", width = 300, height = 100)

    mc.columnLayout (adj = 1)

    mc.checkBoxGrp ("checkTransform", ncb = 4, label = 'matchTransform', la4=['Translate', 'Rotate', 'Scale', 'Pivots'], cal=[1, 'center'])
    mc.button(label='Quick Match', width=300, height=20, c='matchTransform()')
    mc.separator (h=10)
    mc.button(label='Quick Match', width=300, height=20, c='matchTransform()')
    mc.button(label='Parent Constraint', width=300, height=20, c='createParentContraint()')

    mc.showWindow ('qSnap')


def matchTransform(): #Match transforms setups
    sel = mc.ls(sl=True)
    selDriver = sel[0]
    selDriven = sel[1]

    error = 0

    translate = mc.checkBoxGrp ("checkTransform", q=1, v1=True)
    rotate = mc.checkBoxGrp ("checkTransform", q=1, v2=True)
    scale = mc.checkBoxGrp ("checkTransform", q=1, v3=True)
    pivot = mc.checkBoxGrp ("checkTransform", q=1, v4=True)

    if(selDriver == "" or selDriven == ""):
        mc.error("Please select the driver first and then the driven")
        error = 1

    if (error == 0):
        if (translate == 1):
            mc.matchTransform(selDriver, selDriven, pos=True)

    if (error == 0):
        if (rotate == 1):
            mc.matchTransform(selDriver, selDriven, rot=True)

    if (error == 0):
        if (scale == 1):
            mc.matchTransform(selDriver, selDriven, scl=True)

    if (error == 0):
        if (pivot == 1):
            mc.matchTransform(selDriver, selDriven, piv=True)


def createOffsetGroup(): #Adds Offset group
    selection = mc.ls(sl=True)
    selectJoint = selection[0]
    selectController = selection[1]

    if(len(selection) <= 0):
        mc.error ("Select the Parent (Joint) and then the Child (Controller)")
    else:
        selectController = mc.rename(selectController, (selectJoint + "_CTRL"))

    mc.select (selectController)
    mc.makeIdentity (apply=True, t=1, r=1, s=1, n=0, pn=1)
    mc.group (n=(selectController + "_Offset"))

    mc.parentConstraint (selectJoint, (selectController + "_Offset"))

    mc.select(selectController + '_Offset')
    mc.delete(cn=1)


def createParentContraint(): #Create Parent Constraint

    objSel = mc.ls(sl=True)
    parentObj = objSel[0]
    childObj = objSel[1]
    mc.parentConstraint (parentObj, childObj, w=1)
    print ("Parent Constraint Successful")



"""
up_drawingOverides()
"""

def up_drawingOverides(): #UI

    if mc.window('qColor', exists = 1):
        mc.deleteUI('qColor')

    mc.window('qColor', title="up_drawingOverides", width = 300, height = 100)
    mc.columnLayout (adj = 1, cal = "right")
    mc.colorIndexSliderGrp ('mySlider', label = "Select Color", min = 0, max=31, value=0)
    mc.columnLayout (adj = 1, cal = "right")
    mc.separator (h=10)
    mc.button(label='Default', width=150, height=30, al="center",  c= 'defaultColor()')
    mc.button(label='Apply', width=150, height=30, al="center",  c= 'drawingOveride()')
    mc.showWindow ('qColor')

def drawingOveride(): #function for setting up color
    selection = mc.ls(sl=True)
    notSelected = selection
    errorSelected = 0
    sliderQuery = mc.colorIndexSliderGrp("mySlider", q=1, v=True)
    colorIndex = sliderQuery - 1

    if len(notSelected) == 0:
        mc.error("Select 1 or more objects to set a Color")
        errorSelected = 1
    else:
        for select in selection:
            mc.setAttr(select + ".overrideEnabled", 1) 
            mc.setAttr(select + ".overrideColor", colorIndex)


def defaultColor(): #function for setting up default colors
    
    sel = mc.ls(sl=True)

    for s in sel:
        mc.setAttr (s+".overrideEnabled", 1) 
        mc.setAttr (s+".overrideColor", 0) 



"""
up_Connector()
"""

def up_Connector(): #UI

    if mc.window('qConnect', exists = 1):
        mc.deleteUI('qConnect')

    mc.window('qConnect', title="up_Connector", width = 300, height = 100)

    mc.columnLayout (rs = 3)

    mc.checkBoxGrp ("checkTranslate", ncb = 3, label = 'Translation', la3=['x', 'y', 'z'], cal=[1, 'center'])
    mc.checkBoxGrp ("checkRotate", ncb = 3, label = 'Rotation', la3=['x', 'y', 'z'], cal=[1, 'center'])
    mc.checkBoxGrp ("checkScale", ncb = 3, label = 'Scale', la3=['x', 'y', 'z'], cal=[1, 'center'])

    mc.button(label='Connect', width=300, height=30, al="center", c='connector()')
    
    mc.showWindow ('qConnect')

def connector(): # function for connector 
    selection = mc.ls(sl=True)
    selDriver = selection[0]
    selDriven = selection[1]

    error = 0

    #translation data
    tx =  mc.checkBoxGrp("checkTranslate", q=1, v1=True)
    ty =  mc.checkBoxGrp("checkTranslate", q=1, v1=True)
    tz =  mc.checkBoxGrp("checkTranslate", q=1, v1=True)

    #rotation data
    rx =  mc.checkBoxGrp("checkRotate", q=1, v1=True)
    ry =  mc.checkBoxGrp("checkRotate", q=1, v1=True)
    rz =  mc.checkBoxGrp("checkRotate", q=1, v1=True)

    #scale data
    sx =  mc.checkBoxGrp("checkScale", q=1, v1=True)
    sy =  mc.checkBoxGrp("checkScale", q=1, v1=True)
    sz =  mc.checkBoxGrp("checkScale", q=1, v1=True)

    if(selDriver == "" or selDriven == ""):
        mc.error("Select 2 or more Objects. Parent first and then the child")
        error = 1

    #translate
    if (error == 0):
        if (tx == 1):
            mc.connectAttr(selDriver+".translateX", selDriven+".translateX", f=True)
    if (error == 0):
        if (ty == 1):
            mc.connectAttr(selDriver+".translateY", selDriven+".translateY", f=True)
    if (error == 0):
        if (tz == 1):
            mc.connectAttr(selDriver+".translateZ", selDriven+".translateZ", f=True)

    #rotate
    if (error == 0):
        if (rx == 1):
            mc.connectAttr(selDriver+".rotateX", selDriven+".rotateX", f=True)
    if (error == 0):
        if (ry == 1):
            mc.connectAttr(selDriver+".rotateY", selDriven+".rotateY", f=True)
    if (error == 0):
        if (rz == 1):
            mc.connectAttr(selDriver+".rotateZ", selDriven+".rotateZ", f=True)

    #scale
    if (error == 0):
        if (sx == 1):
            mc.connectAttr(selDriver+".scaleX", selDriven+".scaleX", f=True)
    if (error == 0):
        if (sy == 1):
            mc.connectAttr(selDriver+".scaleY", selDriven+".scaleY", f=True)
    if (error == 0):
        if (sz == 1):
            mc.connectAttr(selDriver+".scaleZ", selDriven+".scaleZ", f=True)


def deformerValToOne(): #Deformer weights can cross the max influence value and to bring it to max influence value this function can be used
    defMesh = 'facial_GEO'
    listHis = mc.listHistory(defMesh, ac=1)
    for ech in listHis:
        ndt=mc.nodeType(ech)
        if ndt == 'rig_meshZip' or ndt == 'rig_weightMap':
            print ('working on %s' %ech)
            allVerts = mc.ls('%s.vtx[*]'%defMesh, fl=1)
            for vrt in allVerts:
                weightVal = mc.percent(ech, vrt, q=1, v=1)[0]
                if weightVal > 1.0:
                    print ('%s has weight value more than 1 : value is %s : deformerName : %s' %(vrt, weightVal, ech))
                    mc.percent(ech, vrt, v=1)

                    
                    
def upCentreJoint(): #Create single joint on any vert, edge, face selected 
    b = mc.xform(q=1, bb=1, ws=1)
    centreX = (b[0] + b [3]) / 2
    centreY = (b[1] + b [4]) / 2
    centreZ = (b[2] + b [5]) / 2
    
    jnt = mc.joint(n="joint1", p=[centreX, centreY, centreZ], raidus=1)
    mc.parent=(jnt, ws=1)
