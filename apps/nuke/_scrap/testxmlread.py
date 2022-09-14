import os
from pprint import pprint
from xml.etree import ElementTree as ET

from six.moves import reload_module as reload

import pp_project.project as project
reload(project)

xmlpath = '/homes/talhaa/proj.xml'


def findpref():
    xmltree = ET.parse(xmlpath)
    xmlroot = xmltree.getroot()

    prefSearchExpr = ('applications/application[@name="{}"]/versions/'
                      'version[@name="{}"]/prefs/item[@name="{}"]')

    prefSearchExpr = prefSearchExpr.format(os.environ['SA_APPNAME'],
                                           os.environ['SA_APPVERNAME'],
                                           'format')

    print(('findexpr', prefSearchExpr))

    xmlnode = xmlroot.find(prefSearchExpr)

    pprint(xmlnode.attrib)


def main():
    pd = project.ProjectData(xmlFile=xmlpath)
    value = pd.getApplicationPrefValue(os.environ['SA_APPNAME'],
                                       os.environ['SA_APPVERNAME'], 'format')
    print(value)


if __name__ == '__main__':
    findpref()
    main()
