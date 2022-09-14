from __future__ import print_function

import os
import hiero


import nuke


def print_env(kw='SA_'):
    for key, value in os.environ.items():
        if kw in key:
            print(key, '=', value)


if __name__ == '__main__':
    print_env()
    for path in hiero.core.pluginPath():
        print(path)
    print(hiero)
    import hiero.exporters.FnExternalRender as fn

    print(fn)
