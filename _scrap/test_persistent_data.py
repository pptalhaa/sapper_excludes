import pp_io.util as iopubtuil


import maya.cmds as cmds

for word in cmds.fileInfo(q=True):
    print(word)



items = [{'id': x} for x in range(10)]

print(items)


print({'id': 5} in items)
