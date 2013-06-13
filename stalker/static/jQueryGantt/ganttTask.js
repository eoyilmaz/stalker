/*
 Copyright (c) 2012-2013 Open Lab
 Written by Roberto Bicchierai and Silvia Chelazzi http://roberto.open-lab.com
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/**
 * A method to instantiate valid task models from
 * raw data.
 */
function TaskFactory() {
    /**
     * Build a new Task
     */
    this.build = function (kwargs) {
        kwargs['start'] = kwargs['computed_start'] || kwargs['start'];
        kwargs['end'] = kwargs['computed_end'] || kwargs['end'];
        return new Task(kwargs);
    };
}

function Task(kwargs) {
    this.id = kwargs['id'] || null;
    this.name = kwargs['name'] || null;
    this.code = kwargs['code'] || null;
    this.description = kwargs['description'] || null;
    
    this.priority = kwargs['priority'] || 500;

    this.type = kwargs['type'] || null;

    this.status = "STATUS_UNDEFINED";

    this.project_id = null;

    this.children = [];
    this.child_ids = [];
    this.parent_id = kwargs['parent_id'] || null;
    this.parent = kwargs['parent'] || null;
    this.depend_ids = kwargs['depend_ids'] || [];
    this.depends = null;

    this.start = kwargs['start'] || null;
    this.duration = kwargs['duration'] || null;
    this.end = kwargs['end'] || null;

    this.is_scheduled = kwargs['is_scheduled'] || false;

    this.schedule_model = kwargs['schedule_model'];
    this.schedule_timing = kwargs['schedule_timing'] || 10;
    this.schedule_unit = kwargs['schedule_unit'] || 'h';
    this.schedule_constraint = kwargs['schedule_constraint'] || 0;

    this.schedule_seconds = kwargs['schedule_seconds'] || 0;
    this.total_logged_seconds = kwargs['total_logged_seconds'] || 0;

    this.progress = this.schedule_seconds > 0 ? this.total_logged_seconds / this.schedule_seconds * 100 : 0;

//    console.debug('this.total_logged_seconds : ', this.total_logged_seconds);
//    console.debug('this.schedule_seconds     : ', this.schedule_seconds);
//    console.debug('this.progress             : ', this.progress);

    this.bid_timing = kwargs['bid_timing'] || this.schedule_timing;
    this.bid_unit = kwargs['bid_unit'] || this.schedule_unit;

//    console.debug('schedule_constraint : ', this.schedule_constraint);
//    console.debug('schedule_model      : ', this.schedule_model);
//    console.debug('schedule_timing     : ', this.schedule_timing);
//    console.debug('schedule_unit       : ', this.schedule_unit);
//    console.debug('bid_timing          : ', this.bid_timing);
//    console.debug('bid_unit            : ', this.bid_unit);

    this.is_milestone = false;
    this.startIsMilestone = false;
    this.endIsMilestone = false;

    this.collapsed = false;

    this.rowElement; //row editor html element
    this.ganttElements = []; //gantt html element
    this.master = kwargs['master'] || null;

    this.resources = kwargs['resources'] || [];
    this.resource_ids = kwargs['resource_ids'] || [];
    
    if (this.resource_ids.length == 0){
        // no problem if there are no resources
        for (var i = 0; i < this.resources.length; i++) {
            this.resource_ids.push(this.resources[i].id);
        }
    } else {
        if (this.master != null){
            for (var i = 0; i < this.resource_ids.length; i++){
                this.resources.push(this.master.getResource(this.resource_ids[i]));
            }
        }
    }

    this.timeLogs = [];
    this.timeLog_ids = [];

    // update the duration according to the schedule_timing value
    //this.update_duration_from_schedule_timing();
}

Task.prototype.clone = function () {
    var ret = {};
    for (var key in this) {
        if (typeof(this[key]) != "function") {
            ret[key] = this[key];
        }
    }
    return ret;
};

Task.prototype.getResourcesString = function () {
    var ret = "";
    for (var i = 0; i < this.resources.length; i++) {
        var resource = this.resources[i];
        var res = this.master.getResource(resource.id);
        if (res) {
            ret = ret + (ret == "" ? "" : ", ") + res.name;
        }
    }
    return ret;
};

Task.prototype.getResourcesLinks = function () {
    var ret = "";
    for (var i = 0; i < this.resources.length; i++) {
        ret = ret + (ret == "" ? "" : ", ") + this.resources[i].link();
    }
    return ret;
};

Task.prototype.getDependsLinks = function () {
    var depends = this.getDepends();
    var ret = "";
    for (var i = 0; i < depends.length; i++) {
        ret = ret + (ret == "" ? "" : ", ") + depends[i].link();
    }
    return ret;
};

Task.prototype.link = function () {
    var rendered;
    if (this.type == 'Project') {
        rendered = $.JST.createFromTemplate(this, "PROJECTLINK");
    } else {
        rendered = $.JST.createFromTemplate(this, "TASKLINK");
    }
    return rendered[0].outerHTML;
};


Task.prototype.createResource = function (kwargs) {
    var resource = new Resource(kwargs);
    this.resources.push(resource);
    return resource;
};


//<%---------- TASK STRUCTURE ---------------------- --%>
Task.prototype.getRow = function () {
    var index = -1;
    if (this.master)
        index = this.master.tasks.indexOf(this);
    return index;
};


Task.prototype.getParents = function () {
    var parents = [];
    var current_task = this.getParent();
    while (current_task != null) {
        parents.push(current_task);
        current_task = current_task.parent;
    }
    return parents;
};


Task.prototype.getParent = function () {
    if (this.parent == null && this.parent_id != null) {
        // there should be a parent
        // find the parent from parent_id
        var current_task;

        var parent_index = this.master.task_ids.indexOf(this.parent_id);
        if (parent_index != -1) {
            this.parent = this.master.tasks[parent_index];
            // register the current task as a child of the parent task
            if (this.parent.children.indexOf(this) == -1) {
                this.parent.children.push(this);
            }
        }
    }
    return this.parent;
};


Task.prototype.isParent = function () {
    return this.children.length > 0;
};

Task.prototype.isLeaf = function () {
    return this.children.length == 0;
};


Task.prototype.getChildren = function () {
    return this.children;
};


Task.prototype.getDescendant = function () {
    return this.children;
};

Task.prototype.getDepends = function () {
    if (this.depends == null) {
        this.depends = [];
        if (this.depend_ids.length > 0) {
            // find the tasks
            var dep_id;
            var dep;
            var dep_index;
            for (var i = 0; i < this.depend_ids.length; i++) {
                dep_id = this.depend_ids[i];
                dep_index = this.master.task_ids.indexOf(dep_id);

                if (dep_index != -1) {
                    dep = this.master.tasks[dep_index];
                    this.depends.push(dep);
                    // also update depends_string
                }
            }
        }
    }
    return this.depends;
};

Task.prototype.setDepends = function (depends) {
    // if this is not an array but a string parse it as depends string
    var dependent_task;
    if (typeof(depends) == 'string') {
        // parse it as depends string
        this.depends_string = depends;
        this.depends = [];
        this.depend_ids = [];
        var deps = this.depends_string.split(',');
        var dep_id;
        var depend_index;
        for (var i = 0; i < deps.length; i++) {
            dep_id = deps[i].split(':')[0].trim(); // don't care about the lag
            depend_index = this.master.task_ids.indexOf(dep);
            if (depend_index != -1) {
                dependent_task = this.master.tasks[depend_index];
                this.depends.push(dependent_task);
                this.depend_ids.push(dependent_task.id);
            }
        }
    } else if (depends instanceof Task) {
        // just set it to the depends list
        this.depends = [depends];
        this.depend_ids = [depends.id];
    } else if (depends instanceof Array) {
        // should be an array
        for (var i; i < depends.length; i++) {
            dependent_task = depends[i];
            if (dependent_task instanceof Task) {
                this.depends.push(dependent_task);
                this.depend_ids.push(dependent_task.id);
            }
        }
    }
    // somebody should tell GanttMaster to update the links after this.
};


Task.prototype.getSuperiors = function () {
    // Returns the Tasks that this task depends to.
    return this.getDepends();
};


Task.prototype.getInferiors = function () {
    // Returns the tasks that depends to this task
    var ret = [];
    var task = this;
    if (this.master) {
        ret = this.master.links.filter(function (link) {
            return link.from == task;
        });
    }
    return ret;
};


Task.prototype.update_duration_from_schedule_timing = function () {
    // updates the duration from schedule_timing    
};

Task.prototype.getProgress = function () {
    this.progress = this.schedule_seconds > 0 ? this.total_logged_seconds / this.schedule_seconds * 100 : 0;
    return this.progress;
};

Task.prototype.addTimeLog = function(timeLog) {
    timeLog_id = timeLog.id;
    var index = this.timeLog_ids.indexOf(timeLog_id);
    if (index == -1){
        // it is not in the list
        // update the timeLog
        timeLog.task_id = this.id;
        timeLog.task = this;
        // update self
        this.timeLogs.push(timeLog);
        this.timeLog_ids.push(timeLog_id);
    } // if it is in the list do nothing
};

Task.prototype.addTimeLog_with_id = function(timeLog_id){
    var timeLog = this.master.getTimeLog(timeLog_id);
    this.addTimeLog(timeLog);
};
