from __future__ import print_function
import os
import pp_tracker.tracker as tracker
from collections import defaultdict, OrderedDict

trackers = tracker.Tracker(sudo_as_login=True)
trackers.initTrackers()

shotgun = trackers.trackersDict['shotgun'].sg


def getTasks():
    projectName = os.path.basename(os.environ.get('SA_PROJECTPATH'))
    context = os.environ.get('SA_SCOPE').capitalize()
    assetName = os.environ.get('SA_SCOPEITEM')

    filters = []
    filters.append(('project.Project.name', 'is', projectName))
    filters.append(('entity.%s.code' % context, 'is',
                    assetName.split(':', 1)[-1].replace(':', '_')))

    print(filters)

    tasks = shotgun.find(
        'Task',
        filters=filters,
        fields=['content', 'entity', 'step', 'sg_status_list'],
        order=[{
            'field_name': 'step'
        }])

    steps = shotgun.find('Step',
                         filters=[('entity_type', 'is', context)],
                         fields=['name', 'entity_type', 'list_order', 'color'],
                         order=[{'field_name': 'list_order', 'direction': 'asc'}])

    return tasks


for task in getTasks():
    print(task['content'], task['step'])


# tasks_by_step = defaultdict(list)
# for task in getTasks():
#     step = task['step']
#     tasks_by_step[(task['step']['name'], step['list_order'])].append(task)

# print()
# print('========')
# for step, list_order in tasks_by_step:
#     # print(step, '(%d)' % list_order, ':')
#     for task in tasks_by_step[step]:
#         print('\t', task['content'], ',', task['sg_status_list'])
