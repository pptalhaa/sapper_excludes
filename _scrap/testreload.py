from __future__ import print_function
import os


reload(os)
print('os reloaded', os)


from six.moves import reload_module as reload


reload(os)
print('os reloaded', os)

