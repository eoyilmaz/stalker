# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import logging
from pyramid.httpexceptions import HTTPServerError
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
import transaction

from stalker.db import DBSession
from stalker import User, Task, Entity, log, Project, StatusList, Status, Type

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


def convert_to_depend_index(task, tasks):
    """converts the given task and its dependencies to the format suitable
    for jQueryGantt's depends input
    
    :param task: A Stalker Task
    
    :param [] tasks: A list of Stalker Tasks
    """
    depends = ''
    for dependent_task in task.depends:
        # find the index of the task in the given tasks
        try:
            i = tasks.index(dependent_task)
        except ValueError:
            pass
        else:
            depends += ", %i" % i
    if depends.startswith(','):
        logger.debug('converted to depends: %s' % depends[1:])
        return depends[1:]
    else:
        return ''


def convert_to_jquery_gantt_task_format(tasks):
    """Converts the given tasks to the jQuery Gantt compatible json format.
    
    :param tasks: List of Stalker Tasks.
    :return: json compatible dictionary
    """
    return {
        'tasks' : [
            {
                'id': task.id,
                'name': '%s (%s)' % (task.name, task.entity_type),
                'code': task.id,
                'level': task.level,
                'status': 'STATUS_ACTIVE',
                'start': int(task.start.strftime('%s')) * 1000,
                'duration': task.duration.days,
                'end': int(task.end.strftime('%s')) * 1000,
                'depends': convert_to_depend_index(task, tasks),
                'description': task.description,
                'assigs': [
                    {
                        'resourceId': resource.id,
                        'id': resource.id
                    } for resource in task.resources
                ]
            }
            for task in tasks
        ],
        'resources' : [{
            'id': resource.id,
            'name': resource.name
        } for resource in User.query.all()],
        "canWrite": 1,
        "canWriteOnParent": 1
    }


def update_with_jquery_gantt_task_data(json_data):
    """updates the given tasks in database
    
    :param data: jQueryGantt produced json string
    """
    
    logger.debug(json_data)
    import json
    data = json.loads(json_data)
    
    # Updated Tasks
    for task_data in data['tasks']:
        task_id = task_data['id']
        task_name = task_data['name']
        task_start = task_data['start']
        task_duration = task_data.get('duration', 0)
        task_resource_ids = [resource_data['resourceId']
                             for resource_data in task_data['assigs']]
        task_description = task_data.get('description', '')
        
        # task_depend_ids : " 2, 3, 5, 6:3, 12" these are the index numbers of
        # the task in the Gantt chart, be carefull it is not the id of the task
        task_depend_ids = []
        if len(task_data.get('depends', [])):
            for index_str in task_data['depends'].split(','):
                index = int(index_str.split(':')[0])
                dependent_task_id = data['tasks'][index]['id']
                task_depend_ids.append(dependent_task_id)
        
        # get the task itself
        if not isinstance(task_id, basestring): 
            # update task
            task = Task.query.filter(Task.id==task_id).first()
        elif task_id.startswith('tmp_'):
            # create a new Task
            task = Task()
        
        # update it
        if task:
            task.name = task_name
            task.start = datetime.date.fromtimestamp(task_start/1000)
            task.duration = datetime.timedelta(task_duration)
            
            resources = User.query.filter(User.id.in_(task_resource_ids)).all()
            task.resources = resources
            
            task.description = task_description
            
            task_depends = Task.query.filter(Task.id.in_(task_depend_ids)).all()
            task.depends = task_depends
            DBSession.add(task)
    
    # Deleted tasks
    deleted_tasks = Task.query.filter(Task.id.in_(data['deletedTaskIds'])).all()
    for task in deleted_tasks:
        DBSession.delete(task)
    
    # create new tasks
    
    
    # transaction will handle the commit don't bother doing anything


@view_config(
    route_name='update_tasks',
    renderer='json'
)
def update_tasks(request):
    """updates the given tasks with the given JSON data
    """
    # get the data
    data = request.params['prj']
    if data:
        update_with_jquery_gantt_task_data(data)
    return {}


@view_config(
    route_name='update_task',
    renderer='templates/task/dialog_update_task.jinja2'
)
def update_task(request):
    """runs when updateing a task
    """
    # get logged in user
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    task_id = request.matchdict['task_id']
    task = Task.query.filter(Task.id==task_id).first()
    
    logger.debug('code came here 1')
    if 'submitted' in request.params:
        logger.debug('code came here 2')
        logger.debug(request.params['submitted'])
        if request.params['submitted'] == 'update':
            pass
    
    return {
        'task': task
    }

def depth_first_flatten(task, task_array=None):
    """Does a depth first flattening on the child tasks of the given taks.
    :param task: start from this task
    :param task_array: previous flattened task array
    :return: list of flat tasks
    """
    
    if task_array is None:
        task_array = []
    
    if task:
        if task not in task_array:
            task_array.append(task)
        # take a tour in children
        for child_task in task.children:
            task_array.append(child_task)
            # recursive call
            task_array = depth_first_flatten(child_task, task_array)
    
    return task_array


@view_config(
    route_name='get_tasks',
    renderer='json',
    permission='Read_Task'
)
def get_tasks(request):
    """returns all the tasks in database related to the given entity
    """
    entity_id = request.matchdict.get('entity_id')
    entity = Entity.query.filter_by(id=entity_id).first()
    
    tasks = []
    if entity:
        if entity.entity_type == 'Project':
            project = entity
            # get the tasks who is a root task
            root_tasks = Task.query\
                .filter(Task._project==project)\
                .filter(Task.parent==None).all()
            
            # do a depth first search for child tasks
            for root_task in root_tasks:
                logger.debug('root_task: %s, parent: %s' % (root_task, root_task.parent))
                tasks = depth_first_flatten(root_task)
         
    if log.logging_level == logging.DEBUG:
        logger.debug('tasks count: %i' % len(tasks))
        for task in tasks:
            logger.debug('------------------------------')
            logger.debug('task name: %s' % task.name)
            logger.debug('start date: %s' % task.start)
            logger.debug('end date: %s' % task.end)
    
    return convert_to_jquery_gantt_task_format(tasks)


@view_config(
    route_name='get_project_tasks',
    renderer='json',
    permission='Read_Task'
)
def get_project_tasks(request):
    """returns all the tasks of the given Project instance
    """
    project_id = request.matchdict.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    tasks = None
    if project:
        tasks = project.project_tasks
    
    return [
        {
            'id': task.id,
            'name': '%s (%s in %s)' % (task.name,
                                       task.task_of.name,
                                       task.task_of.project.name),
        }
        for task in tasks
    ]


@view_config(
    route_name='view_tasks',
    renderer='templates/task/content_list_tasks.jinja2',
    permission='Read_Task'
)
def view_tasks(request):
    """runs when viewing tasks of a TaskableEntity
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter(Entity.id==entity_id).first()
    
    return {
        'entity': entity
    }


@view_config(
    route_name='create_task',
    renderer='templates/task/dialog_create_task.jinja2',
    permission='Create_Task'
)
def create_task(request):
    """runs when adding a new task
    """
    
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'create':
            if 'parent_id' in request.params and \
                'name' in request.params and \
                'description' in request.params and \
                'is_milestone' in request.params and \
                'resource_ids' in request.params and \
                'status_id' in request.params:
                
                # get the taskable entity
                parent_id = request.params['parent_id']
                parent = Entity.query.filter_by(id=parent_id).first()
                kwargs = {}
                if parent.entity_type == 'Project':
                    kwargs.update({'project': parent})
                else:
                    kwargs.update({'parent': parent})
                
                # get the status_list
                status_list = StatusList.query.filter_by(
                    target_entity_type='Task'
                ).first()
                
                logger.debug('status_list: %s' % status_list)
                
                # there should be a status_list
                if status_list is None:
                    return HTTPServerError(
                        detail='No StatusList found'
                    )
                
                status_id = int(request.params['status_id'])
                logger.debug('status_id: %s' % status_id)
                status = Status.query.filter_by(id=status_id).first()
                logger.debug('status: %s' % status)
                
                # get the resources
                resource_ids = [
                    int(r_id)
                    for r_id in request.POST.getall('resource_ids')
                ]
                resources = User.query.filter(User.id.in_(resource_ids)).all()
                
                # get the dates
                # TODO: no time zone info here, please add time zone
                start = datetime.datetime.strptime(
                    request.params['start'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )
                start_time = datetime.datetime.strptime(
                    request.params['start_time'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )
                end = datetime.datetime.strptime(
                    request.params['end'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )
                end_time = datetime.datetime.strptime(
                    request.params['end_time'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )
                # update the hour and minute of start from start time
                start = start.replace(
                    hour=start_time.hour,
                    minute=start_time.minute
                )
                end = end.replace(
                    hour=end_time.hour,
                    minute=end_time.minute
                )
                
                logger.debug('start : %s' % start)
                logger.debug('end : %s' % end)
                
                # get the dependencies
                depend_ids = [
                    int(d_id)
                    for d_id in request.POST.getall('depend_ids')
                ]
                depends = Task.query.filter(Task.id.in_(depend_ids)).all()
                logger.debug('depends: %s' % depends)
                
                kwargs.update(dict(
                    name=request.params['name'],
                    status_list=status_list,
                    status=status,
                    created_by=logged_in_user,
                    start=start,
                    end=end,
                    resources=resources,
                    depends=depends
                ))
                
                try:
                    new_task = Task(**kwargs)
                    logger.debug('new_task.status: ' % new_task.status)
                    DBSession.add(new_task)
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_task)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Task')
                        #return {}
            else:
                logger.debug('there are missing parameters')
                def get_param(param):
                    if param in request.params:
                        logger.debug('%s: %s' % (param, request.params[param]))
                    else:
                        logger.debug('%s not in params' % param)
                get_param('task_of_id')
                get_param('name')
                get_param('description')
                get_param('is_milestone')
                get_param('resource_ids')
                get_param('status_id')
    
    # return the necessary values to prepare the form
    # get the taskable entity
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()
    
    return {
        'entity': entity,
        'types': Type.query.filter_by(target_entity_type='Task').all(),
        'users': User.query.all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Task').first()
    }


@view_config(
    route_name='get_user_tasks',
    renderer='json'
)
def get_user_tasks(request):
    """returns the user tasks as jQueryGantt json
    """
    # get user id
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()
    
    # get tasks
    tasks = []
    if user is not None:
        tasks = sorted(user.tasks, key=lambda x: x.project.id)
    
    return convert_to_jquery_gantt_task_format(tasks)
