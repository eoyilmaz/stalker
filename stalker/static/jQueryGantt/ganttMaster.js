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
function GanttMaster() {
    this.tasks = [];
    this.task_ids = []; // lookup table for quick task access

    this.deletedTaskIds = [];
    this.links = [];

    this.editor; //element for editor
    this.gantt; //element for gantt

    this.element;

    this.resources; //list of resources
    this.resource_ids; //lookup table for quick resource access

    this.minEditableDate = 0;
    this.maxEditableDate = Infinity;
    
    this.minDate = new Date();
    this.maxDate = new Date();

    this.timing_resolution = 3600000; // as miliseconds, for now it is 1 hour

    // this is in minutes from midnight because Stalker is designed in that way
    this.working_hours = {
        'mon': [
            [540, 1080]
        ],
        'tue': [
            [540, 1080]
        ],
        'wed': [
            [540, 1080]
        ],
        'thu': [
            [540, 1080]
        ],
        'fri': [
            [540, 1080]
        ],
        'sat': [],
        'sun': []
    };

    this.start = new Date().getTime();
    this.end = new Date().getTime();

    this.daily_working_hours = 9; // this is the default
    this.weekly_working_hours = 45;
    this.weekly_working_days = 5;
    this.yearly_working_days = 260.714; // 5 * 52.1428

    this.canWriteOnParent = true;
    this.canWrite = true;

    this.firstDayOfWeek = Date.firstDayOfWeek;

    this.currentTask; // task currently selected;

    this.__currentTransaction;  // a transaction object holds previous state during changes
//    this.__undoStack = [];
//    this.__redoStack = [];


    this.task_link_template;
    this.resource_link_template;

    var self = this;
}

GanttMaster.prototype.init = function (place) {
    this.element = place;

    var self = this;

    //load templates
    $("#gantEditorTemplates").loadTemplates().remove();  // TODO: Remove inline jquery, this should be injected

    //create editor
    this.editor = new GridEditor(this);
    this.editor.element.width(place.width() * .9 - 10);
    place.append(this.editor.element);

    //create gantt
//    this.gantt = new Ganttalendar("m", new Date().getTime() - 3600000 * 24 * 2, new Date().getTime() + 3600000 * 24 * 15, this, place.width() * .6);
    this.gantt = new Ganttalendar('m', this.start, this.end, this, place.width() * .6);

    //setup splitter
    var splitter = $.splittify.init(place, this.editor.element, this.gantt.element, 50);
    splitter.secondBox.css("overflow-y", "auto").scroll(function () {
        splitter.firstBox.scrollTop(splitter.secondBox.scrollTop());
    });

    //bindings
    place.bind("refreshTasks.gantt",function () {
        self.redrawTasks();
    }).bind("refreshTask.gantt",function (e, task) {
            self.drawTask(task);
    }).bind("zoomPlus.gantt",function () {
            self.gantt.zoomGantt(true);
    }).bind("zoomMinus.gantt", function () {
            self.gantt.zoomGantt(false);
    });
};

GanttMaster.messages = {
    "CHANGE_OUT_OF_SCOPE": "NO_RIGHTS_FOR_UPDATE_PARENTS_OUT_OF_EDITOR_SCOPE",
    "START_IS_MILESTONE": "START_IS_MILESTONE",
    "END_IS_MILESTONE": "END_IS_MILESTONE",
    "TASK_HAS_CONSTRAINTS": "TASK_HAS_CONSTRAINTS",
    "GANTT_ERROR_DEPENDS_ON_OPEN_TASK": "GANTT_ERROR_DEPENDS_ON_OPEN_TASK",
    "GANTT_ERROR_DESCENDANT_OF_CLOSED_TASK": "GANTT_ERROR_DESCENDANT_OF_CLOSED_TASK",
    "TASK_HAS_EXTERNAL_DEPS": "TASK_HAS_EXTERNAL_DEPS",
    "GANTT_ERROR_LOADING_DATA_TASK_REMOVED": "GANTT_ERROR_LOADING_DATA_TASK_REMOVED",
    "CIRCULAR_REFERENCE": "CIRCULAR_REFERENCE",
    "ERROR_SETTING_DATES": "ERROR_SETTING_DATES",
    "CANNOT_DEPENDS_ON_ANCESTORS": "CANNOT_DEPENDS_ON_ANCESTORS",
    "CANNOT_DEPENDS_ON_DESCENDANTS": "CANNOT_DEPENDS_ON_DESCENDANTS",
    "INVALID_DATE_FORMAT": "INVALID_DATE_FORMAT",
    "GANTT_QUARTER_SHORT": "GANTT_QUARTER_SHORT",
    "GANTT_SEMESTER_SHORT": "GANTT_SEMESTER_SHORT"
};


GanttMaster.prototype.createTask = function (kwargs) {
    var factory = new TaskFactory();
    return factory.build(kwargs);
};


GanttMaster.prototype.createResource = function (kwargs) {
    return new Resource(kwargs);
};


//update depends strings
GanttMaster.prototype.updateDepends = function () {
    //remove all deps
    for (var i = 0; i < this.tasks.length; i++) {
        this.tasks[i].depends = [];
    }

    for (var i = 0; i < this.links.length; i++) {
        var link = this.links[i];
        link.to.depends.push(link.from.id);
    }
};



/**
 * a ganttData contains tasks, resources, roles
 * @param ganttData
 * @param Deferred
 */
GanttMaster.prototype.loadGanttData = function (ganttData, Deferred) {
    var deferred = new Deferred;
    this.beginTransaction();
    this.resources = ganttData.resources;
    this.resource_ids = [];
    for (var i = 0; i < this.resources.length; i++) {
        this.resource_ids.push(this.resources[i].id);
    }

    this.timing_resolution = ganttData.timing_resolution || this.timing_resolution;
    this.working_hours = ganttData.working_hours || this.working_hours;
    this.daily_working_hours = ganttData.daily_working_hours || this.daily_working_hours;
    this.weekly_working_hours = ganttData.weekly_working_hours || this.weekly_working_hours;
    this.weekly_working_days = ganttData.weekly_working_days || this.weekly_working_days;
    
    this.start = ganttData.start || -1;
    this.end = ganttData.end || -1;
    this.gantt.originalStartMillis = ganttData.start;
    this.gantt.originalEndMillis = ganttData.end;

    this.canWrite = ganttData.canWrite;
    this.canWriteOnParent = ganttData.canWriteOnParent;

    if (ganttData.minEditableDate)
        this.minEditableDate = computeStart(ganttData.minEditableDate);
    else
        this.minEditableDate = -Infinity;

    if (ganttData.maxEditableDate)
        this.maxEditableDate = computeEnd(ganttData.maxEditableDate);
    else
        this.maxEditableDate = Infinity;


    this.loadTasks(ganttData.tasks);
    this.deletedTaskIds = [];
    this.endTransaction();
    var self = this;
    
    // TODO: this is ridiculous, it should start when something is finished, not after a certain time
    this.gantt.element.oneTime(200, function () {
        self.gantt.centerOnToday();
        deferred.resolve('success');
    });

//    console.debug('daily_working_hours : ', this.daily_working_hours);
//    console.debug('timing_resolution   : ', this.timing_resolution);
//    console.debug('working_hours       : ', this.working_hours);

    return deferred.promise;
};


GanttMaster.prototype.loadTasks = function (tasks) {
    var factory = new TaskFactory();
    //reset
    this.reset();

    var task;
    for (var i = 0; i < tasks.length; i++) {
        task = tasks[i];
        if (!(task instanceof Task)) {
            var t = factory.build({
                id: task.id,
                name: task.name,
                code: task.code,
                description: task.description,
                priority: task.priorty,
                type: task.type,
                status: task.status,
                parent_id: task.parent_id,
                depend_ids: task.depend_ids,
                depends: null,
                resources: task.resources,
                start: task.start,
                duration: task.duration,
                end: task.end,
                bid_timing: task.bid_timing,
                bid_unit: task.bid_unit,
                is_scheduled: task.is_scheduled,
                is_milestone: task.is_milestone,
                computed_start: task.computed_start,
                computed_end: task.computed_end,
                schedule_constraint: task.schedule_constraint,
                schedule_model: task.schedule_model,
                schedule_timing: task.schedule_timing,
                schedule_unit: task.schedule_unit,
                schedule_seconds: task.schedule_seconds,
                total_logged_seconds: task.total_logged_seconds
            });

            // TODO: do it properly
            for (var key in task) {
                if (key != "end" && key != "start")
                    t[key] = task[key]; //copy all properties
            }
            task = t;
        }
        task.master = this; // in order to access controller from task

        task.depends = null;
        this.tasks.push(task);  //append task at the end
        this.task_ids.push(task.id); //lookup table for task ids
    }

//    console.debug('this.tasks    : ', this.tasks);
//    console.debug('this.task_ids : ', this.task_ids);

    // find root tasks
    var root_tasks = [];
    for (var i = 0; i < this.tasks.length; i++) {
        // just find root tasks
        // also register parents
        if (this.tasks[i].getParent() == null) {
            root_tasks.push(this.tasks[i]);
        }
        // also fill the task.depends
        this.tasks[i].getDepends();
//        console.debug('task.depend_ids : ', this.tasks[i].depend_ids);
//        console.debug('task.depends    : ', this.tasks[i].depends);
    }


    var loop_through_child = function (task, children) {
        if (children == null) {
            children = []
        }
        children.push(task);
        var current_task_children = task.getChildren();
        for (var n = 0; n < current_task_children.length; n++) {
            children = loop_through_child(current_task_children[n], children);
        }
        return children;
    };


    var sorted_task_list = [];
    // now go from root to child
    for (var i = 0; i < root_tasks.length; i++) {
        sorted_task_list = loop_through_child(root_tasks[i], sorted_task_list);
    }

    // update tasks
    this.tasks = sorted_task_list;
    // update the lookup table
    this.task_ids = [];
    for (var i = 0; i < this.tasks.length; i++) {
        this.task_ids.push(this.tasks[i].id);
    }
    // set the first task selected
    this.currentTask = this.tasks[0];

    //var prof=new Profiler("gm_loadTasks_addTaskLoop");
    for (var i = 0; i < this.tasks.length; i++) {
        task = this.tasks[i];

        //add Link collection in memory
        var linkLoops = !this.updateLinks(task);

        if (linkLoops) {
            alert(GanttMaster.messages.GANNT_ERROR_LOADING_DATA_TASK_REMOVED + "\n" + task.name + "\n" +
                (linkLoops ? GanttMaster.messages.CIRCULAR_REFERENCE : GanttMaster.messages.ERROR_SETTING_DATES));

            //remove task from in-memory collection
            var task_index = this.task_ids.indexOf(task.id);
            this.tasks.splice(task_index, 1);
            this.task_ids.splice(task_index, 1);
        } else {
            //append task to editor
            this.editor.addTask(task);
            //append task to gantt
//            this.gantt.addTask(task);
        }
    }

//    this.editor.fillEmptyLines();
    //prof.stop();
};


GanttMaster.prototype.getTask = function (taskId) {
    if (typeof(taskId) == 'string') {
        taskId = parseInt(taskId);
    }
    var task_index = this.task_ids.indexOf(taskId);
    return this.tasks[task_index];
};


GanttMaster.prototype.getResource = function (resId) {
    var resource_index = this.resource_ids.indexOf(resId);
    return this.resources[resource_index];
};


GanttMaster.prototype.taskIsChanged = function () {
    //console.debug("taskIsChanged");
    var master = this;

    //refresh is executed only once every 50ms
    this.element.stopTime("gnnttaskIsChanged");
    //var profilerext = new Profiler("gm_taskIsChangedRequest");
    this.element.oneTime(50, "gnnttaskIsChanged", function () {
        //console.debug("task Is Changed real call to redraw");
        //var profiler = new Profiler("gm_taskIsChangedReal");
        master.editor.redraw();
        master.gantt.refreshGantt();
        //profiler.stop();
    });
    //profilerext.stop();
};


GanttMaster.prototype.redraw = function () {
    this.editor.redraw();
    this.gantt.refreshGantt();
};

GanttMaster.prototype.reset = function () {
    this.tasks = [];
    this.task_ids = [];
    this.links = [];
    this.deletedTaskIds = [];
    delete this.currentTask;

    this.editor.reset();
    this.gantt.reset();
};


GanttMaster.prototype.saveGantt = function (forTransaction) {
    //var prof = new Profiler("gm_saveGantt");
    var saved = [];
    for (var i = 0; i < this.tasks.length; i++) {
        var task = this.tasks[i];

        // skip if project
        if (task.type == 'Project') {
            continue;
        }

        var cloned = task.clone();
        delete cloned.master;
        delete cloned.rowElement;
        delete cloned.ganttElement;

        delete cloned.children;
        //delete cloned.resources;
        delete cloned.depends;
        delete cloned.parent;

        saved.push(cloned);
    }

    var ret = {tasks: saved};

    ret.deletedTaskIds = this.deletedTaskIds;  //this must be consistent with transactions and undo

    if (!forTransaction) {
        ret.resources = this.resources;
        ret.canWrite = this.canWrite;
        ret.canWriteOnParent = this.canWriteOnParent;
    }

    //prof.stop();
    return ret;
};


GanttMaster.prototype.updateLinks = function (task) {
    //console.debug("updateLinks");
    
    //remove my depends
    this.links = this.links.filter(function (link) {
        return link.to != task;
    });

    var todoOk = true;

    // just update the depends list
    if (task.getDepends().length > 0) {
        //cannot depend from an ancestor
        var parents = task.getParents();
        //cannot depend from descendants
        var descendants = task.getDescendant();

        var deps = task.depends;
        var newDepsString = "";

        var visited = [];
        for (var j = 0; j < deps.length; j++) {
            var dep = deps[j];
            var lag = 0;

            if (dep) {
                this.links.push(new Link(dep, task, lag));
                newDepsString = newDepsString + (newDepsString.length > 0 ? "," : "") + dep;
            }
        }

        task.depends_string = newDepsString;

    }
    //prof.stop();
    return todoOk;
};


//<%----------------------------- TRANSACTION MANAGEMENT ---------------------------------%>
GanttMaster.prototype.beginTransaction = function () {
    if (!this.__currentTransaction) {
        this.__currentTransaction = {
//            snapshot: JSON.stringify(this.saveGantt(true)),
            errors: []
        };
    } else {
        console.error("Cannot open twice a transaction");
    }
    return this.__currentTransaction;
};


GanttMaster.prototype.endTransaction = function () {
    if (!this.__currentTransaction) {
        console.error("Transaction never started.");
        return true;
    }

    var ret = true;

    this.gantt.originalStartMillis = this.start;
    this.gantt.originalEndMillis = this.end;
    
    this.taskIsChanged(); //enqueue for gantt refresh
    this.__currentTransaction = undefined;

    return ret;
};

//this function notify an error to a transaction -> transaction will rollback
GanttMaster.prototype.setErrorOnTransaction = function (errorMessage, task) {
    if (this.__currentTransaction) {
        this.__currentTransaction.errors.push({msg: errorMessage, task: task});
    } else {
        console.error(errorMessage);
    }
};

// inhibit undo-redo
GanttMaster.prototype.checkpoint = function () {
    this.__undoStack = [];
    this.__redoStack = [];
};

GanttMaster.prototype.getDateInterval = function(){
    var start = Infinity;
    var end = -Infinity;
    for (var i = 0; i < this.tasks.length; i++) {
        var task = this.tasks[i];
        if (task.type == 'Project'){
            continue;
        }
        if (start > task.start)
            start = task.start;
        if (end < task.end)
            end = task.end;
    }
    if (start == Infinity){
        start = new Date(new Date().getTime() - 1296000000);
    }
    if (end == -Infinity){
        end = new Date(new Date().getTime() + 1296000000);
    }
    this.minDate = start;
    this.maxDate = end;
    return {
        start: this.minDate,
        end: this.maxDate
    }
};
