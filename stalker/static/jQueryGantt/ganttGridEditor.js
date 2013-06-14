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
function GridEditor(master) {
    this.master = master; // is the a GanttEditor instance
    var gridEditor;
    if (this.master.grid_mode == 'Task'){
//        console.debug('GridEditor.__init__: this.master.grid_mode = Task');
        gridEditor = $.JST.createFromTemplate({}, "TASKSEDITHEAD");
    } else if (this.master.grid_mode == 'Resource') {
//        console.debug('GridEditor.__init__: this.master.grid_mode = Resource');
        gridEditor = $.JST.createFromTemplate({}, "RESOURCESEDITHEAD");
    }
    gridEditor.gridify();
    this.element = gridEditor;
}


GridEditor.prototype.addTask = function (task) {
//    console.debug('GridEditor.addTask start');
    var taskRow;
    if (task.type == 'Task' || task.type == 'Asset' || task.type == 'Shot' ||
        task.type == 'Sequence') {
        if (!task.isParent()) {
            taskRow = $.JST.createFromTemplate(task, "TASKROW");
        } else {
            taskRow = $.JST.createFromTemplate(task, "PARENTTASKROW");
        }
    } else if (task.type == 'Project') {
        taskRow = $.JST.createFromTemplate(task, "PROJECTROW");
    }

    //save row element on task
    task.rowElement = taskRow;

    this.element.append(taskRow);

//    console.debug('GridEditor.addTask end');
    return taskRow;
};

GridEditor.prototype.addResource = function (resource) {
//    console.debug('GridEditor.addResource start');
    var resourceRow = $.JST.createFromTemplate(resource, "RESOURCEROW");

    //save row element on resource
    resource.rowElement = resourceRow;
    this.element.append(resourceRow);

//    console.debug('GridEditor.addResource rowElement: ', resourceRow);
//    console.debug('GridEditor.addResource end');
    return resourceRow;
};



GridEditor.prototype.refreshRowIndices = function () {
//    console.debug('GridEditor.refreshRowIndices start');
    if (this.master.grid_mode=='Task'){
//        console.debug('GridEditor.refreshRowIndices in Task mode');
        this.element.find(".taskRowIndex").each(function (i, el) {
            $(el).html(i + 1);
        });
    } else if (this.master.grid_mode == 'Resource'){
//        console.debug('GridEditor.refreshRowIndices in Resource mode');
        this.element.find(".resourceRowIndex").each(function (i, el) {
            $(el).html(i + 1);
        });
    }
//    console.debug('GridEditor.refreshRowIndices end');
};


GridEditor.prototype.refreshTaskRow = function (task) {
    //console.debug("refreshTaskRow")
    //var profiler = new Profiler("editorRefreshTaskRow");
    var row = task.rowElement;
//    console.debug('GridEditor.refreshTaskRow, row:', task, row);

    row.find(".taskRowIndex").html(task.getRow() + 1);
    row.find(".indentCell").css("padding-left", task.getParents().length * 10);
    row.find(".name").html(task.name);
    row.find(".code").html(task.code);
//    row.find("[status]").attr("status", task.status);

    row.find(".timing").html(task.schedule_model.toUpperCase()[0] + ":" + task.schedule_timing + task.schedule_unit);
    row.find(".start").html(new Date(task.start).format("yyyy-mm-dd HH:00")).updateOldValue(); // called on dates only because for other field is called on focus event
    row.find(".end").html(new Date(task.end).format("yyyy-mm-dd HH:00")).updateOldValue();

//    var dep_string = '';
//    for (var i = 0; i < task.getDepends().length; i++) {
//        dep_string = '' + task.depends[i].name + ', ';
//    }
//    row.find("[name=depends]").val(dep_string);
//    row.find(".taskResources").html(task.getResourcesString());

    //profiler.stop();
};


GridEditor.prototype.refreshResourceRow = function (resource) {
    var row = resource.rowElement;
//    console.debug('GridEditor.refreshResourceRow: row:', row);
//    console.debug('GridEditor.refreshResourceRow: row.find(".resourceRowIndex"):', row.find(".resourceRowIndex"));
//    console.debug('GridEditor.refreshResourceRow: resource.getRow(): ', resource.getRow());
    row.find(".resourceRowIndex").html(resource.getRow() + 1);
    row.find(".id").html(resource.id);
    row.find(".name").html(resource.name);
};




GridEditor.prototype.redraw = function () {
//    console.debug('GridEditor.redraw start');
    if (this.master.grid_mode == 'Task'){
//        console.debug('GridEditor.redraw in Task mode');
        for (var i = 0; i < this.master.tasks.length; i++) {
            this.refreshTaskRow(this.master.tasks[i]);
        }
    } else if (this.master.grid_mode == 'Resource'){
//        console.debug('GridEditor.redraw in Resource mode');
//        console.debug('this.master.resources.length: ', this.master.resources.length);
        for (var i = 0; i < this.master.resources.length; i++) {
            this.refreshResourceRow(this.master.resources[i]);
        }
    }
//    console.debug('GridEditor.redraw end');
};


GridEditor.prototype.reset = function () {
//    console.debug('GridEditor.reset start');
    this.element.find("[dataId]").remove();
//    console.debug('GridEditor.reset end');
};
