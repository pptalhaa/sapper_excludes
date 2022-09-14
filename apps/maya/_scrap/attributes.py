import maya.cmds as cmds
import maya.mel as mel


for attr in cmds.attributeInfo('defaultArnoldRenderOptions', all=True):
    print(attr)




print(cmds.getAttr('defaultArnoldRenderOptions.imageFormat'))

print(cmds.listConnections('defaultArnoldRenderOptions.drivers'))


print(cmds.attributeInfo('defaultArnoldDisplayDriver', all=True))



print(cmds.getAttr('defaultArnoldDisplayDriver.aiTranslator'))


print(cmds.getAttr('defaultRenderGlobals.imfkey'))



print(mel.eval('getImfImageType()'))
