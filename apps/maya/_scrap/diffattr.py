from __future__ import print_function
import maya.cmds as cmds
import mtoa.aovs as aaovs


for name, node in aaovs.getAOVNodes(names=True):
    print()
    print(node, ":")
    for attr in cmds.attributeInfo(node, all=True):
        try:
            val = cmds.getAttr(node + '.' + attr)
        except(RuntimeError, ValueError):
            continue
        print ('\t', attr, '=', val)




# for aov in aaovs.getAOVs():
#     for i in dir(aov):
#         if '_' in i:
#             continue
#         print(aov, i, getattr(aov, i))
