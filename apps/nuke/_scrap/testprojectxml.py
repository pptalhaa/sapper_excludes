from __future__ import print_function

from pp_utils import uxml

import os
import xml.etree.ElementTree as et

import pprint
import StringIO

testxml = '''
<projectData>
    <applications>
        <application name="maya">
            <prefs>
                <pref key="department" value="anim"/>
                <pref key="res" value="hd"/>
            </prefs>
        </application>
        <application name="nuke">
        </application>
        <application name="rv">
            <prefs>
                <pref key="res" value="hd"/>
                <pref key="department" value="prod"/>
            </prefs>
        </application>
    </applications>
</projectData>
'''

xmldata = StringIO.StringIO(testxml)


def print_env(kw=''):
    for key, value in os.environ.items():
        if kw in key:
            print(key, '=', value)


def print_node(node, attrib=False, children=False):
    '''
    :type node: et.Element
    '''
    print(node.tag)
    if attrib:
        pprint.pprint(node.attrib)
    if children:
        pprint.pprint(node.getchildren())


def getProjectXML(projectPath=None):
    if projectPath is None:
        projectPath = os.environ.get('SA_PROJECTPATH')
    return os.path.join(os.environ['SA_PROJECTPATH'], '_sys', 'config',
                        'projectData.xml')


def findCurrentAppVersion(xmltree):
    nuke = None
    for nuke in xmltree.getroot().findall(
            ('applications/application[@name="{SA_APPNAME}"]'
             '/versions/version[@name="{SA_APPVERNAME}"]').format(**(os.environ))):
        return nuke



import pp_project.project as project


print_env('SA_')
pd = project.ProjectData(xmlFile='/homes/talhaa/testpd.xml')
pref = pd.setApplicationPrefValue('nuke', '12_2v6', 'format', 'QHD')
k = pd.getApplicationPrefValue('nuke', '12_2v6', 'format')
print(k)

pd.projectData.write('/homes/talhaa/testpd.xml')
print('fileWritter')


