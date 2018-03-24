'''
Author: Miguel Angel Luna Armada

This tool enhances the extrusion of multiple curves using the same profile
The Maya native UI passes a single argument to the functions thats way they require a "clicked" argument
'''

import maya.cmds as cmds

first_object = []
second_objects = []


def storeSelection(arrayToStore):
    if arrayToStore:
        del arrayToStore[:]
    selection = cmds.ls(selection=True, flatten=True)
    for i in selection:
        first_object.append(i)


def storeShapes(arrayToStore):
    if arrayToStore:
        del arrayToStore[:]
    selection = cmds.ls(selection=True, flatten=True)
    shapes = cmds.listRelatives(selection, shapes=True)
    for i in shapes:
        second_objects.append(i)


def CurveExtruder(profileArray, shapesArray):
    polygonTypeQuery = cmds.optionMenu("OutputTypeQuery", query=True, value=0)
    rotationValue = cmds.intField("RotateAlongValue", query=True, value=True)

    if polygonTypeQuery == "NURBS":
        polygonTypeQuery = 0
    else:
        polygonTypeQuery = 1

    for curva in shapesArray:
        cmds.select(curva)
        cmds.extrude(profileArray[0], curva, extrudeType=2, fixedPath=True, useComponentPivot=1, useProfileNormal=True,
                     constructionHistory=False, polygon=polygonTypeQuery, rotation=rotationValue)
        cmds.delete(constructionHistory=True)

def CurveExtruder_UI():
    '''
	Script main UI where you can select the objects you need to process and stuff
	'''
    if cmds.window("ScriptUIWindow", exists=True):
        cmds.deleteUI("ScriptUIWindow")

    cmds.window("ScriptUIWindow", title="MLA Curve Extruder", iconName='Curve Extruder', sizeable=True,
                width=100, height=100)
    cmds.columnLayout("ScriptUIWindow")
    cmds.columnLayout()
    cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(150, 30))

    cmds.optionMenu("OutputTypeQuery", label='Output Type')
    cmds.menuItem(label='Polygons')
    cmds.menuItem(label='NURBS')
    cmds.separator(style='none')

    cmds.button(label='Store extrude profile', command='storeSelection(first_object)')
    cmds.button(label='Store curves', command='storeShapes(second_objects)')

    cmds.text(label='Rotate along curve amount')
    cmds.intField("RotateAlongValue", minValue=0, maxValue=360, value=0)

    cmds.separator(style='none')
    cmds.separator(style='none')

    cmds.button(label='Extrude!', command='CurveExtruder(first_object, second_objects)')
    cmds.button(label='Close', width=70, height=20, command='cmds.deleteUI("ScriptUIWindow")')
    cmds.showWindow("ScriptUIWindow")


if __name__ == "__main__":
    CurveExtruder_UI()
