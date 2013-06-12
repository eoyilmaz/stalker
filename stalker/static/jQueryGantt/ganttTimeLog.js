// Stalker a Production Asset Management System
// Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation;
// version 2.1 of the License.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

function TimeLog(kwargs) {
    this.id = kwargs['id'] || null;

    this.task_id = kwargs['task_id'] || null;
    this.task = kwargs['task'] || null;

    this.resource_id = kwargs['resource_id'] || null;
    this.resource = kwargs['resource'] || null;

    this.start = kwargs['start'] || null;
    this.end = kwargs['end'] || null;

    this.rowElement = null; // row editor html element of the resource
    this.ganttElement = null; // gantt html element

    this.master = null;
}

TimeLog.prototype.getResource = function(){
    // getter for the resource
    if (this.resource == null){
        this.resource = this.master.getResource(this.resource_id);
        this.rowElement = this.resource.rowElement;
    }
    return this.resource;
};

TimeLog.prototype.setResource = function(resource_id){
    // set the resource with id
    this.resource_id = resource_id;
    this.resource = this.master.getResource(resource_id);
};

TimeLog.prototype.getTask = function(){
    // getter for the task
    if (this.task == null){
        this.task = this.master.getTask(this.task_id);
    }
    return this.task;
};

TimeLog.prototype.setTask = function(task_id){
    // set the task with id
    this.task_id = task_id;
    this.task = this.master.getTask(task_id);
    // also update the task
    this.task.addTimeLog(this);
};

