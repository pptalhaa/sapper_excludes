from __future__ import print_function

import os
import glob
import pprint
import json

import pp_publishing.pub as pub
import pp_publishing.pub_db as pub_db
import pp_publishing.pub_dirs as pub_dirs
from pp_nodes.read_group import cleanExtAndFrame

# for key, value in os.environ.items():
#     if 'sa_' in key.lower():
#         print(key, '=', value)

pubd = {}
pubd['project'] = os.environ.get('SA_PROJECTNAME')
pubd['scope'] = os.environ.get('SA_SCOPE')
pubd['shot'] = '%s_%s' % (os.environ.get('SA_SEQUENCE'),
                          os.environ.get('SA_SHOT'))
pubd['tag'] = 'environment_L10_beauty'
pubd['version'] = pub.getLatestVersionNumber(pubd)


versions = pub.getAllVersions(pubd)


# for v in versions:
#     print()
#     for key, value in v.items():
#         print(key, '=', repr(value))


mainPath = versions[0]['filepath']

beautyPath = mainPath
ext = os.path.splitext(beautyPath)[-1]
paddedExt = beautyPath.split(".", 1)[-1]

dirName = os.path.dirname(beautyPath)

files = glob.glob(dirName+"/*"+ext)

aovset = set()
for filename in files:
    if os.path.isfile(filename):
        filename = filename.replace(os.path.sep, "/")
        aovset.add(cleanExtAndFrame(filename))

passBasePath = beautyPath.rsplit("_", 2)[0]
masterName = cleanExtAndFrame(os.path.basename(mainPath))
fromStr = pub_dirs.getPubDictFromStr(mainPath)
fromStr.pop('stage')
pdvide = pub_db.query(fromStr)[0]


print('masterName', masterName)
print('passBasePath', passBasePath)
print('paddedExt', paddedExt)

aovs = sorted(list(aovset))
metadata = pub_db.getMetadata(pdvide)
deep_data = json.loads(metadata.get('deep_data', '[]'))


passBasename = os.path.basename(passBasePath)
print('passBasename', passBasename)
deep_aovs = [
        cleanExtAndFrame(d).replace(passBasename, "").rsplit('_', 1)[0][1:]
        for d in deep_data]
pprint.pprint(deep_aovs)

