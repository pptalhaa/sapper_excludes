from __future__ import print_function

import datetime
import copy
import json

from collections import OrderedDict

import pp_tracker.trackers.shotgun.pp_shotgun as pp_shotgun
from pp_project import lister, project

from pprint import pprint

pp_sg = pp_shotgun.PP_Shotgun(sudo_as_login=True)
sg = pp_sg.sg


def getTaskStatuses():
    task_status_schema = sg.schema_field_read('Task', 'sg_status_list')
    return task_status_schema['sg_status_list']['properties']['display_values']['value']


def getProjectDepartments(projectPath):
    pd = project.ProjectData(projectPath=projectPath)
    result = OrderedDict()
    for scope in ('asset', 'shot'):
        deps = pd.getDepartments(appSpecific=False, scope=scope)
        result[scope] = OrderedDict(zip(deps, [[]]*len(deps)))
    return result


def updateDepartmentSummary(summary, update):
    final_summary = copy.deepcopy(summary)
    for scope in ('asset', 'shot'):
        if scope not in final_summary:
            final_summary[scope] = OrderedDict()
        final_summary[scope].update(update[scope])
    return final_summary


def getDepartmentSummary():
    project_paths = lister.ProjectLister().getProjectPaths()

    deps_summary = OrderedDict()
    for pname, ppath in project_paths.items():
        try:
            projDeps = getProjectDepartments(ppath)
            deps_summary = updateDepartmentSummary(deps_summary, projDeps)
        except AttributeError:
            pass

    return deps_summary


def getStepSummary():
    filters = []
    filters.append({
        'filter_operator':
        'any',
        'filters': [('entity', 'type_is', 'Asset'),
                    ('entity', 'type_is', 'Shot')]
    })
    filters.append(
            ('created_at', 'greater_than', datetime.datetime.now() -
                datetime.timedelta(days=365 * 2)))
    tasks = sg.find('Task',
                    filters=filters,
                    fields=['project', 'content', 'entity', 'created_at',
                        'step'],
                    order=[{'field_name': 'created_at', 'direction': 'desc'}])
    steps_summary = {'Asset': [], 'Shot': []}
    for task in tasks:
        scope = task['entity']['type']
        if not task['step']:
            continue
        if task['step']['name'] not in steps_summary[scope]:
            steps_summary[scope].append(task['step']['name'])
    return steps_summary


def getStepTasks(entity_type, step_name):
    print('Getting tasks for %s' % step_name)
    tasks = sg.find(
            'Task',
            filters=[
                ('step.Step.code', 'is', step_name),
                ('step.Step.entity_type', 'is', entity_type)],
            fields=['content'])
    task_names = set([t['content'] for t in tasks])
    return task_names


def getStepSummary2(with_step_tasks=False):
    filters = []
    filters.append(('entity_type', 'in', ['Asset', 'Shot']))
    fields = ['code', 'list_order', 'entity_type', 'department']
    steps = sg.find('Step', filters=filters, fields=fields,
            order=[{'field_name': 'entity_type'}, {'field_name': 'list_order'}])
    stepsDict = OrderedDict()
    for step in steps:
        entity_type = step['entity_type']
        department = step['department'] and step['department']['name']
        name = step['code']
        if entity_type not in stepsDict:
            stepsDict[entity_type] = OrderedDict()
        if department not in stepsDict[entity_type]:
            stepsDict[entity_type][department] = OrderedDict()
        stepsDict[entity_type][department][name] = list(
                getStepTasks(entity_type, name)) if with_step_tasks else []
    return stepsDict


if __name__ == '__main__':
    ddata = OrderedDict()
    ddata['shotgun task statuses'] = getTaskStatuses()
    ddata['project departments'] = getDepartmentSummary()
    ddata['shotgun departments, steps and tasks'] = getStepSummary2()

    with open(os.path.join(os.path.dirname(pp_shotgun.__file__),
        'shotgun_raw_task_data.json'), 'w') as _file:
        json.dump(ddata, _file, indent=2)

    getTaskStatuses()
