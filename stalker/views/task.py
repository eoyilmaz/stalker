# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


import datetime
import json

from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPServerError, HTTPOk


import transaction
from sqlalchemy.exc import IntegrityError

from stalker.db import DBSession
from stalker import User, Task, Entity, Project, StatusList, Status
from stalker.models.task import CircularDependencyError

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
            depends += ",%i" % (i+1) # depends is 1-based where i is 0-based
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
    data = {
        'tasks' : [
            {
                'id': task.id,
                'name': '%s (%s)' % (task.name, task.entity_type),
                'code': task.id,
                'parent_id': task.parent.id if task.parent else None,
                'status': 'STATUS_UNDEFINED',
                'start': int(task.start.strftime('%s')) * 1000,
                'duration': task.duration.days,
                'end': int(task.end.strftime('%s')) * 1000,
                'depends_ids': [dep.id for dep in task.depends],#convert_to_depend_index(task, tasks),
                'description': task.description,
                'resources': [
                    {
                        'id': resource.id,
                    } for resource in task.resources
                ]
            }
            for task in tasks
        ],
        'resources' : [{
            'id': resource.id,
            'name': resource.name
        } for resource in User.query.all()],
        # "canWrite": 0,
        # "canWriteOnParent": 0
    }
    
    logger.debug('loading gantt data:\n%s' % 
                 json.dumps(data,
                            sort_keys=False,
                            indent=4,
                            separators=(',', ': ')
                 )
    )
    return data
    


def update_with_jquery_gantt_task_data(json_data):
    """updates the given tasks in database
    
    :param data: jQueryGantt produced json string
    """
    
    logger.debug(json_data)
    data = json.loads(json_data)
    
    logger.debug('updating tasks with gantt data:\n%s' % 
                 json.dumps(data,
                            sort_keys=False,
                            indent=4,
                            separators=(',', ': ')
                 )
    )
    
    
    task_name_replace_strs = [
        ' (Task)', ' (Project)', ' (Asset)', ' (Sequence)', ' (Shot)'
    ]
    
    # Updated Tasks
    for task_data in data['tasks']:
        logger.debug('*********************************************')
        task_id = task_data['id']
        task_name = task_data['name'] # just take the part without 
                                      # the parenthesis
        for rstr in task_name_replace_strs:
            if task_name.endswith(rstr):
                task_name = task_name[:-len(rstr)]
        
        task_start = task_data['start']
        task_duration = task_data.get('duration', 0)
        task_resource_ids = [resource_data['id']
                             for resource_data in task_data['resources']]
        task_description = task_data.get('description', '')
        
        # no need to update parent, it will only be possible by using
        # Stalker's own task edit UI
        # 
        #task_parent = task_data.get('parent_id', '')
        
        # --------
        # Updated:
        # --------
        # task depend_ids are now real Stalker task id, no need to convert it
        # to something else
        # task_depend_ids : " 2, 3, 5, 6:3, 12" these are the ids of the task
        task_depend_ids = []
        if len(task_data.get('depends', [])):
            for index_str in task_data['depends'].split(','):
                dependent_task_id = int(index_str.split(':')[0])
                logger.debug('index : %s' % dependent_task_id)
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
            logger.debug('task %s' % task)
            task.name = task_name
            logger.debug('task.start given (raw)  : %s' % task_start)
            logger.debug('task.start given (calc) : %s' % datetime.datetime.fromtimestamp(task_start/1000))
            task.start = datetime.datetime.fromtimestamp(task_start/1000)
            logger.debug('task.start after set    : %s' % task.start)
            task.duration = datetime.timedelta(task_duration)
            
            resources = User.query.filter(User.id.in_(task_resource_ids)).all()
            task.resources = resources
            
            task.description = task_description
            
            task_depends = Task.query.filter(Task.id.in_(task_depend_ids)).all()
            
            logger.debug('task.parent : %s' % task.parent)
            logger.debug('task_depends: %s' % task_depends)
            
            task.depends = task_depends
            DBSession.add(task)
    
    logger.debug('*********************************************')
    
    # Deleted tasks
    deleted_tasks = Task.query.filter(Task.id.in_(data['deletedTaskIds'])).all()
    for task in deleted_tasks:
        DBSession.delete(task)
    
    # create new tasks
    
    
    # transaction will handle the commit don't bother doing anything


@view_config(
    route_name='update_gantt_tasks',
    renderer='json'
)
def update_gantt_tasks(request):
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
    """runs when updating a task
    """
    # get logged in user
    login = authenticated_userid(request)
    # logged_in_user = User.query.filter_by(login=login).first()
    
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
    route_name='get_root_tasks',
    renderer='json',
)
def get_root_tasks(request):
    """returns all the root tasks in the database related to the given project
    """
    project_id = request.matchdict.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    
    tasks = []
    
    root_tasks = Task.query\
                .filter(Task._project==project)\
                .filter(Task.parent==None).all()
    
    # do a depth first search for child tasks
    for root_task in root_tasks:
        logger.debug('root_task: %s, parent: %s' % (root_task, root_task.parent))
        tasks.extend(depth_first_flatten(root_task))
    
    return convert_to_jquery_gantt_task_format(tasks) 

@view_config(
    route_name='get_gantt_tasks',
    renderer='json',
    permission='List_Task'
)
def get_gantt_tasks(request):
    """returns all the tasks in the database related to the given entity in
    jQueryGantt compatible json format
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
                tasks.extend(depth_first_flatten(root_task))
        elif entity.entity_type == 'User':
            user = entity
            
            # sort the tasks with the project.id
            if user is not None:
                tasks = sorted(user.tasks, key=lambda task: task.project.id)
    
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
    permission='List_Task'
)
def get_project_tasks(request):
    """returns all the tasks in the database related to the given entity in
    flat json format
    """
    # get all the tasks related in the given project
    project_id = request.matchdict.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    
    return [
        {
            'id': task.id,
            'name': '%s (%s)' % (task.name,
                                       task.entity_type),
        } for task in Task.query.filter(Task._project==project).all()]


@view_config(
    route_name='list_tasks',
    renderer='templates/task/content_list_tasks.jinja2',
    permission='Read_Task'
)
def list_tasks(request):
    """runs when viewing tasks of a TaskableEntity
    """
    login = authenticated_userid(request)
    # logged_in_user = User.query.filter_by(login=login).first()
    
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter(Entity.id==entity_id).first()
    
    return {
        'entity': entity
    }



@view_config(
    route_name='create_task_dialog',
    renderer='templates/task/dialog_create_task.jinja2',
    permission='Create_Task'
)
def create_task_dialog(request):
    """only project information is present
    """
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    
    return {
        'project': project
    }


@view_config(
    route_name='create_child_task_dialog',
    renderer='templates/task/dialog_create_task.jinja2',
    permission='Create_Task'
)
def create_child_task_dialog(request):
    """generates the info from the given parent task
    """
    parent_task_id = request.matchdict['task_id']
    parent_task = Task.query.filter_by(id=parent_task_id).first()
    
    project = parent_task.project if parent_task else None
    
    return {
        'project': project,
        'parent': parent_task,
    }


@view_config(
    route_name='create_dependent_task_dialog',
    renderer='templates/task/dialog_create_task.jinja2',
    permission='Create_Task'
)
def create_dependent_task_dialog(request):
    """runs when adding a dependent task
    """
    # get the dependee task
    depends_to_task_id = request.matchdict['task_id']
    depends_to_task = Task.query.filter_by(id=depends_to_task_id).first()
    
    project = depends_to_task.project if depends_to_task else None
    
    return {
        'project': project,
        'depends_to': depends_to_task
    }


def get_datetime(request, date_attr, time_attr):
    """Extracts a datetime object from the given request
    :param request: the request object
    :param date_attr: the attribute name
    :return: datetime.datetime
    """
    # TODO: no time zone info here, please add time zone
    date_part = datetime.datetime.strptime(
        request.params[date_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )
    time_part = datetime.datetime.strptime(
        request.params[time_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )
    # update the time values of date_part with time_part
    return date_part.replace(
        hour=time_part.hour,
        minute=time_part.minute,
        second=time_part.second,
        microsecond=time_part.microsecond
    )


@view_config(
    route_name='create_task',
    permission='Create_Task'
)
def create_task(request):
    """runs when adding a new task
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    project_id = request.params.get('project_id', None)
    name = request.params.get('name', None)
    is_milestone = request.params.get('is_milestone', None)
    status_id = request.params.get('status_id', None)
    parent_id = request.params.get('parent_id', None)
    
    kwargs = {}
    
    if project_id and name and is_milestone and status_id:
        
        # get the project
        project = Project.query.filter_by(id=project_id).first()
        kwargs['project'] = project
        
        # get the parent if exists
        parent = None
        if parent_id:
            parent = Task.query.filter_by(id=parent_id).first()
        
        kwargs['parent'] = parent
        
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
        resources = []
        if 'resource_ids' in request.params:
            resource_ids = [
                int(r_id)
                for r_id in request.POST.getall('resource_ids')
            ]
            resources = User.query.filter(User.id.in_(resource_ids)).all()
        
        # get the dates
        start = get_datetime(request, 'start_date', 'start_time')
        end = get_datetime(request, 'end_date', 'end_time')
        
        logger.debug('start : %s' % start)
        logger.debug('end : %s' % end)
        
        # get the dependencies
        depend_ids = [
            int(d_id)
            for d_id in request.POST.getall('depend_ids')
        ]
        depends = Task.query.filter(Task.id.in_(depend_ids)).all()
        logger.debug('depends: %s' % depends)
        
        kwargs['name'] = name
        kwargs['status_list'] = status_list
        kwargs['status'] = status
        kwargs['created_by'] = logged_in_user
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['resources'] = resources
        kwargs['depends'] = depends
        
        try:
            new_task = Task(**kwargs)
            logger.debug('new_task.name %s' % new_task.name)
            logger.debug('new_task.status: %s' % new_task.status)
            DBSession.add(new_task)
        except (AttributeError, TypeError, CircularDependencyError) as e:
            logger.debug(e.message)
            error = HTTPServerError()
            error.title = str(type(e))
            error.detail = e.message
            return error
        else:
            DBSession.add(new_task)
            try:
                transaction.commit()
            except IntegrityError as e:
                logger.debug(e.message)
                transaction.abort()
                return HTTPServerError(detail=e.message)
            else:
                logger.debug('flushing the DBSession, no problem here!')
                DBSession.flush()
                logger.debug('finished adding Task')
    else:
        logger.debug('there are missing parameters')
        def get_param(param):
            if param in request.params:
                logger.debug('%s: %s' % (param, request.params[param]))
            else:
                logger.debug('%s not in params' % param)
        get_param('project_id')
        get_param('name')
        get_param('description')
        get_param('is_milestone')
        get_param('resource_ids')
        get_param('status_id')
        
        param_list = ['project_id', 'name', 'description',
                      'is_milestone', 'resource_ids', 'status_id']
 
        params = [param for param in param_list if param not in request.params]
        
        error = HTTPServerError()
        error.explanation = 'There are missing parameters: %s' % params
        return error
    
    return HTTPOk(detail='Task created successfully')


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
