import maya.cmds as cmds
from MLA_MayaUtils.ScriptUI import ScriptUI
from MLA_MayaUtils.Selections import Selection


firstHalfOfMeshUVs = []
secondHalfOfMeshUVs = []

def cleanArray(arrayname):
	if arrayname:
		del arrayname[:]

def storeUVs(arraytoStore):
	cleanArray(arraytoStore)
	cmds.ConvertSelectionToUVs()
	selected = Selection.getSelected()

	for uv in selected:
		arraytoStore.append(uv)

def guessSecondSelection():
	cleanArray(secondHalfOfMeshUVs)
	cmds.ConvertSelectionToUVs()
	selected = Selection.getSelected()

	for uv in selected:
		if uv in firstHalfOfMeshUVs:
			continue
		else:
			secondHalfOfMeshUVs.append(uv)
	cmds.select(secondHalfOfMeshUVs)

def moveUVHorizontal(value):
	cmds.polyEditUV(relative= False, uValue= value)

def moveUVVertical (value):
	cmds.polyEditUV(relative= False, vValue= value)


def autoMap(uvMin, uvMax, proporcion=1, firstHalfOfMeshUVArray=firstHalfOfMeshUVs, secondHalfOfMeshUVArray=secondHalfOfMeshUVs):
	'''
	Cycles through two lists of uv ids.
	First action gets the mapping in the desired horizontal position
	Second action distributes the vertices vertically through an unfold method
	'''
	for uv in firstHalfOfMeshUVArray:
		cmds.select (uv, replace=True)
		moveUVHorizontal(uvMin)

	for uv in secondHalfOfMeshUVArray:
		cmds.select(uv, replace=True)
		moveUVHorizontal(uvMax)

	cmds.select(firstHalfOfMeshUVArray, replace=True)
	cmds.select(secondHalfOfMeshUVArray, add=True)
	cmds.unfold(iterations=10000, optimizeAxis=1, globalMethodBlend=0, stoppingThreshold=0, globalBlend=0, pinUvBorder=0, useScale=False)
	corregirProporcionAutomap(proporcion)

def corregirProporcionAutomap (proporcion):
	cmds.polyEditUV( pivotU=0.0, pivotV=0.0, scaleV=proporcion)

if __name__ == "__main__":
	scriptWindow = ScriptUI("Automapper", "automapper")
	scriptWindow.addLayout()
	scriptWindow.addButton("Store first selection", 'storeUVs(firstHalfOfMeshUVs)')
	scriptWindow.addButton("Store second selection", 'storeUVs(secondHalfOfMeshUVs)')
	scriptWindow.addButton("Guess second selection", 'guessSecondSelection()')
	scriptWindow.addSeparator()
	scriptWindow.addText("Umin, Umax and proportion")
	scriptWindow.addSeparator()
	scriptWindow.addField("float", "UVmin")
	scriptWindow.addField("float", "UVmax")
	scriptWindow.addField("float", "UVproportion")

	cmds.floatField("UVmin", edit=True, value=0.004)
	cmds.floatField("UVmax", edit=True, value=0.271)
	cmds.floatField("UVproportion", edit=True, value=3.3)
	scriptWindow.addButton("Automap this shit", 'autoMap(scriptWindow.queryField("float", "UVmin"), scriptWindow.queryField("float", "UVmax"), scriptWindow.queryField("float", "UVproportion"))')
	scriptWindow.show()
