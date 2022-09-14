from __future__ import print_function
from os import wait


import copy

import nuke
import json

root = nuke.root()

print(root.name(), root.Class())

format_knob = root.knob("format")
old_format = format_knob.value()

def print_format(format):
    print(format_tcl(format))


def format_tcl(format):
    return '%d %d %d %d %d %d %f %s' % (
            format.width(), format.height(),
            format.x(), format.y(),
            format.r(), format.t(),
            format.pixelAspect(),
            format.name()
            )


def format_copy(format):
    new_format = nuke.Format(
        format.width(), format.height(),
        format.x(), format.y(),
        format.r(), format.t(),
        format.pixelAspect())
    return new_format


padding = 200


# nuke.addFormat(format_tcl(new_format))
#
#
print()
print('formats')
for format in nuke.formats():
    if format.name() == 'square_1K':
        format.setWidth(1000)
        format.setHeight(1000)
    print_format(format)

print()
print('formats')
for format in nuke.formats():
    print_format(format)

print()




format_knob.setValue('myFullHD')

