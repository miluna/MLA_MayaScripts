first_object_pivot = []
first_object_position = []


def getSelected():
    return cmds.ls(selection=True, flatten=True)


def getFirstSelection(transform="pivot", list=first_object_pivot):
    if list:
        del list[:]

    if transform == "pivot":
        transformation = cmds.xform(getSelected(), query=True, rotatePivot=True)
    if transform == "position":
        transformation = cmds.xform(getSelected(), query=True, translation=True)

    if transformation is not None:
        for number in transformation:
            list.append(number)


def xformPaste(transform="pivot", list=first_object_pivot):
    if transform == "pivot":
        cmds.xform(getSelected(), rotatePivot=[list[0], list[1], list[2]])
    if transform == "position":
        cmds.xform(getSelected(), translation=[list[0], list[1], list[2]])



def CopyPivot_UI():
    '''
    Script main UI where you can select the objects you need to process and stuff
    '''
    if cmds.window("ScriptUIWindow", exists=True):
        DeleteUI_onClick()

    cmds.window("ScriptUIWindow", title="MLA Copy Pivot", iconName='Copy Pivot', sizeable=True)
    cmds.columnLayout("ScriptUIWindow")
    cmds.columnLayout()
    cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(150, 30))

    cmds.button(label='Copy pivot', command='getFirstSelection("pivot", first_object_pivot)')
    cmds.button(label='Paste Pivot', command='xformPaste("pivot", first_object_pivot)')
    cmds.button(label='Copy Position', command='getFirstSelection("position", first_object_position)')
    cmds.button(label='Paste Position', command='xformPaste("position", first_object_position)')

    cmds.separator(style='none')
    cmds.separator(style='none')

    cmds.button(label='Paste Piv as Pos', command='xformPaste("position", first_object_pivot)')
    cmds.button(label='Paste Pos as Piv', command='xformPaste("pivot", first_object_position)')

    cmds.separator(style='none')
    cmds.separator(style='none')

    cmds.separator(style='none')
    cmds.button(label='Close', command='cmds.deleteUI("ScriptUIWindow")')
    cmds.showWindow("ScriptUIWindow")


if __name__ == "__main__":
    CopyPivot_UI()
