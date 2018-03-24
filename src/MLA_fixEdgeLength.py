'''
Author: Miguel Angel Luna

This script is designed to correct the edge length given a user value to make multiple edges uniform
'''

import maya.cmds as cmds
import math


def fixEdgeLength(edge, targetLength):
    '''
    Single edge length correction calculus
    '''
    cmds.select(edge)
    sel = cmds.ls(sl=True, fl=True)
    cmds.ConvertSelectionToVertices()

    p = cmds.xform(sel, q=True, t=True, ws=True)
    length = math.sqrt(math.pow(p[0] - p[3], 2) + math.pow(p[1] - p[4], 2) + math.pow(p[2] - p[5], 2))
    cmds.select(sel)
    scaleLength = ((targetLength * 100) / length) / 100
    cmds.polyMoveEdge(sel, localScaleX=scaleLength)
    print 'Previous Edge Length=' + str(length) + "\tTarget length=" + str(targetLength) + "\tScaled " + str(
        scaleLength),


def fixEdgeLengthProcess():
    '''
    Used to fix multiple edges at the same time and collecting the UI values
    '''
    selection = cmds.ls(sl=True, fl=True)
    targetLength = cmds.intFieldGrp("targetLength", query=True, value1=True)

    for edge in selection:
        fixEdgeLength(edge, targetLength)


def ScriptUI():
    '''
    Script main UI
    '''
    if cmds.window("ScriptUIWindow", exists=True):
        cmds.deleteUI("ScriptUIWindow")

    ScriptUIWindow = cmds.window("ScriptUIWindow", title="Fix edge length script by MLA", iconName='Fix edge length',
                                 sizeable=True)
    cmds.columnLayout("ScriptUIWindow")

    cmds.text(label="Select any edge you want to fix, enter a value and press the button")
    cmds.separator(style='none')
    cmds.intFieldGrp("targetLength", label='Target Length', value1=1)

    cmds.rowLayout(numberOfColumns=4, columnWidth3=(80, 75, 150), adjustableColumn=2, columnAlign=(1, 'right'),
                   columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])

    fixLengthBtn = cmds.button(label='Fix edge length', command='fixEdgeLengthProcess()')
    closeBtn = cmds.button(label='Close', command='cmds.deleteUI("ScriptUIWindow")')
    cmds.showWindow("ScriptUIWindow")


if __name__ == "__main__":
    ScriptUI()
