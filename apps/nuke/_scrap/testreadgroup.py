from __future__ import print_function
import os

import nuke
import nukescripts

import pp_publishing.pub as pub
import pp_publishing.pub_db as pub_db
reload(pub_db)
import pp_publishing.pub_dirs as pub_dirs


from six.moves import reload_module as reload


import pp_nodes.read_group as read_group
reload(read_group)

import pp_nodes.write as write
reload(write)

import pp_io.import_funcs as impf
reload(impf)

import pp_io.update_funcs as updf
reload(updf)

import pp_io.util as util
reload(util)

import pprint


def cleanup():
    for node in nuke.allNodes():
        nuke.delete(node)


def test_create_render():
    pubd = {}
    pubd['project'] = os.environ.get('SA_PROJECTNAME')
    pubd['scope'] = os.environ.get('SA_SCOPE')
    pubd['shot'] = '%s_%s' % (os.environ.get('SA_SEQUENCE'),
                            os.environ.get('SA_SHOT'))
    pubd['tag'] = 'character_L10_beauty'
    pubd['version'] = pub.getLatestVersionNumber(pubd)


    versions = pub_db.query(pubd)

    pd = versions[0]
    pd['filepath'] = pub_dirs.getProjectAbsPath(pd['filepath'])

    # read_group.createReadGroup('TestReadGroup', pub[])
    grp = impf.importRender(versions[0], None)
    nukescripts.clear_selection_recursive()
    grp.setSelected(True)
    write.create_PPWrite()

    for dn in read_group.getDeepReadNodes(grp, False):
        nukescripts.clear_selection_recursive()
        dn.setSelected(True)
        write.create_PPWrite()


def test_create_comp():
    pubd = {}
    pubd['project'] = os.environ.get('SA_PROJECTNAME')
    pubd['scope'] = os.environ.get('SA_SCOPE')
    pubd['shot'] = '%s_%s' % (os.environ.get('SA_SEQUENCE'),
                            os.environ.get('SA_SHOT'))
    pubd['type'] = 'comp'
    pubd['tag'] = 'deep'
    pubd['version'] = pub.getLatestVersionNumber(pubd)
    versions = pub_db.query(pubd)
    pd = versions[0]
    pd['filepath'] = pub_dirs.getProjectAbsPath(pd['filepath'])

    grp = impf.importRender(pd, None)
    nukescripts.clear_selection_recursive()
    grp.setSelected(True)
    write.create_PPWrite()
    for dn in read_group.getDeepReadNodes(grp, False):
        nukescripts.clear_selection_recursive()
        dn.setSelected(True)
        write.create_PPWrite()


def test_update():
    pubnodes = util.getScenePublishingNodes()
    for node in pubnodes:
        pubDict = util.getPublishingData(node)
        updf.updatePublishingNode(node, pubDict, {})


cleanup()
test_create_comp()
test_create_render()
test_update()


# vim: ft=python
