from __future__ import print_function
from os import wait


from StringIO import StringIO

import xml.etree.ElementTree as ET

from pp_utils import uxml

def formatFromTcl(tcl):
    '''Creates a format object from tcl format string as described in
    nuke.addFormat nuke pythonreference

    :type tcl: str
    :rtype: nuke.Format
    '''

    # pat = r'(?P<width>\d+)\s+(?P<height>\d+)\s+((?P<x>\d+)\s+(?P<y>\d+)\s+(?P<r>\d+)\s+(?P<t>\d+)\s+)?((?P<pa>\d+\.\d+)\s+)?(?P<name>.+)'
    hw_pat = r'(?P<width>\d+)\s+(?P<height>\d+)\s+'
    ia_pattern = r'((?P<x>\d+)\s+(?P<y>\d+)\s+(?P<r>\d+)\s+(?P<t>\d+)\s+)?'
    pa_pattern = r'((?P<pa>\d+\.\d+)\s+)?'
    name_pattern = r'(?P<name>.+)'
    pattern = hw_pat + ia_pattern + pa_pattern + name_pattern

    splits = tcl.split()
    name = splits[-1]
    params = splits[:-1]

    # width and height
    params[0] = int(params[0])
    params[1] = int(params[1])

    # x,y,r,t
    if len(params) >= 6:
        for x in range(2, 6):
            params[x] = int(params[x])
    else:
        params.insert(2, 0)
        params.insert(3, 0)
        params.insert(4, params[0])
        params.insert(5, params[1])

    if len(params) in (3, 7):
        params[-1] = float(params[-1])

    format = nuke.Format(*params)
    format.setName(name)
    return format

xmltext = '''<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''

xmlio = StringIO(xmltext)

xmltree = ET.parse(xmlio)
xmlroot = xmltree.getroot()

for rank in xmlroot.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'true')

print('----')
ET.dump(xmlroot)


for country in xmlroot.findall('country'):
    rank = int(country.find('rank').text)
    if rank > 50:
        xmlroot.remove(country)

print('----')
ET.dump(xmlroot)


pakistan = ET.SubElement(xmlroot, 'country')
pakistan.set('name', 'Pakistan')
ET.SubElement(pakistan, 'rank').text = '100'
ET.SubElement(pakistan, 'year').text = '2016'
ET.SubElement(pakistan, 'gdppc').text = '5000'
n1 = ET.SubElement(pakistan, 'neighbor')
n1.set('direction', 'E')
n1.set('name', 'India')

s = StringIO()
uxml.indent(xmlroot)
xmltree.write(s)

print('----')
print(s)
print(s.getvalue())

