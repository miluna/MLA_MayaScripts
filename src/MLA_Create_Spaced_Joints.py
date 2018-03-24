'''
Author: Miguel Angel Luna Armada

This Python script is used to create perfectly spaced joints between two bones. Select start and end bones and run the script with the desired number of joints
'''
import maya.cmds as cmds

# This condition solves a bug in Maya 2016 where if you say trackSelectionOrder=True and it is already true, breaks the selection order
if not cmds.selectPref(query=True, trackSelectionOrder=True):
    cmds.selectPref(trackSelectionOrder=True)


def create_spaced_joints(clicked):
    selected = cmds.ls(orderedSelection=True)

    firstJointPos = cmds.xform(selected[0], query=True, worldSpace=True, translation=True)
    lastJointPos = cmds.xform(selected[1], query=True, worldSpace=True, translation=True)

    numberofnewjoints = cmds.intFieldGrp("Spacing_Field", query=True, value1=True)
    jointSpacingX = (lastJointPos[0] - firstJointPos[0]) / numberofnewjoints
    jointSpacingY = (lastJointPos[1] - firstJointPos[1]) / numberofnewjoints
    jointSpacingZ = (lastJointPos[2] - firstJointPos[2]) / numberofnewjoints

    cmds.select(selected[0])
    i = 1
    for bone in range(0, numberofnewjoints):
        cmds.joint(position=(str(firstJointPos[0] + (jointSpacingX * i)), str(firstJointPos[1] + (jointSpacingY * i)),
                             str(firstJointPos[2] + (jointSpacingZ * i))))
        i += 1
    cmds.delete(selected[1])


def create_spaced_joints_UI():
    '''
    Script main UI where you select the number of joints to create and run the script
    '''
    if cmds.window("ScriptUIWindow", exists=True):
        cmds.deleteUI("ScriptUIWindow")

    cmds.window("ScriptUIWindow", title="Create Spaced Joints ", iconName='Create Spaced Joints',
                sizeable=True)
    cmds.columnLayout("ScriptUIWindow")
    cmds.columnLayout()
    cmds.text("Select first and last bone and replace this chain for: ")
    cmds.intFieldGrp("Spacing_Field", label='Number of new joints', value1=4)
    cmds.rowLayout(numberOfColumns=2, columnWidth3=(80, 75, 150), adjustableColumn=2, columnAlign=(1, 'right'),
                   columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
    cmds.button(label='Create', command='create_spaced_joints()')
    cmds.button(label='Close', command='cmds.deleteUI("ScriptUIWindow")')
    cmds.showWindow("ScriptUIWindow")


if __name__ == "__main__":
    create_spaced_joints_UI()
