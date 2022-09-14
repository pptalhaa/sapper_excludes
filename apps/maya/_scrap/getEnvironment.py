import os


import pp_tracker.tracker as pp_tracker

trackers = pp_tracker.Tracker()


print()
for key, value in os.environ.items():
    if 'stage' in key.lower() or 'dep' in key.lower():
        print("{}={}".format(key, value))
