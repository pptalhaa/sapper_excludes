from __future__ import print_function

from pprint import pprint
import os
import json

import pp_publishing.pub_db as pub_db
import pp_publishing.pub as pub

os.environ['SA_DEBUGDB'] = 'false'


def getRenderDict():
    pubdict = {
        'project': os.environ.get('SA_PROJECTNAME'),
        'scope': os.environ.get('SA_SCOPE'),
        'shot': '{}_{}'.format(os.environ.get('SA_SEQUENCE'),
                               os.environ.get('SA_SHOT')),
    }
    pubdict['type'] = 'render'
    pubdict['tag'] = 'character_L10_Beauty'
    return pubdict


pubdict = getRenderDict()
print()
print(pubdict)
versions = pub.getAllVersions(pubdict)
versions = sorted(versions, key=lambda x: x['version'])


v = versions[-1]

metadata = pub_db.getMetadata(v)


json.loads(metadata.get('deep_data', json.dumps([])))


dirname = os.path.dirname(v['filepath'])
basename = os.path.basename(v['filepath'])


basename = basename.rsplit('.', 2)[0]
basename = basename.rsplit('_', 2)[0]


print(basename)
