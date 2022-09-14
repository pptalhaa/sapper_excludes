from __future__ import print_function
import maya.cmds as cmds


import pp_io.util as pu

reload(pu)


for layer in cmds.renderSetup(q=True, renderLayers=True):
    print(layer, pu.getDeepRenderPasses(layer))
