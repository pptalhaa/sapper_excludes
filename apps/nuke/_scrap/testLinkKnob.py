import nuke
import pprint


nodes = nuke.allNodes()


for n in nodes:
    nuke.delete(n)

cb = nuke.nodes.CheckerBoard()

for i in range(5):
    readNode = nuke.nodes.Read()
    readNode.knob('xpos').setValue(int(cb.knob('xpos').value() + 100 * i))
    readNode.knob('ypos').setValue(int(cb.knob('ypos').value() + 100    ))

    readNode.addKnob(nuke.Link_Knob('cbNode', 'CheckerBoardNode'))

    kname = 'readNode_%s' % readNode.name()
    cb.addKnob(nuke.Link_Knob(kname))
    cb.knob(kname).setLink('%s.%s' % (readNode.name(), 'disable'))


for name, knob in cb.knobs().items():
    if name.startswith('readNode'):
        node = knob.node()
        pprint.pprint((node.__repr__(), knob, node.knob(name), node.knob(name).node()))

readNode.setName('heck')

print()
print()
print()
for name, knob in cb.knobs().items():
    if name.startswith('readNode'):
        print(knob.getLinkedKnob())
        node = knob.node()
        pprint.pprint((node.__repr__(), knob, node.knob(name), node.knob(name).node()))

