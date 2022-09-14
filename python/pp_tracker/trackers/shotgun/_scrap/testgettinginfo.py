from __future__ import print_function

import os

import pp_tracker.trackers.shotgun.pp_shotgun as pp_shotgun

reload(pp_shotgun)

from shotgun.api.v3_0_40.shotgun import Shotgun


shotgun = Shotgun(pp_shotgun.SHOTGUN_URL,
                  pp_shotgun.sa_test[0],
                  pp_shotgun.sa_test[1],
                  sudo_as_login='talhaa')


for key, value in os.environ.items():
    if key.startswith('SA_'):
        print(key, '=', value)


for field, field_info in shotgun.schema_entity_read('Task').items():
    if field == 'Status':
        print(field, field_info)
