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
    var gridEditor = $.JST.createFromTemplate({}, "TASKSEDITHEAD");
    gridEditor.gridify();
    this.element = gridEditor;
}


GridEditor.prototype.addTask = function (task) {
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

    return taskRow;
};


GridEditor.prototype.refreshRowIndices = function () {
    this.element.find(".taskRowIndex").each(function (i, el) {
        $(el).html(i + 1);
    });
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
    row.find(".start").html(new Date(task.start).format()).updateOldValue(); // called on dates only because for other field is called on focus event
    row.find(".end").html(new Date(task.end).format()).updateOldValue();

    var dep_string = '';
    for (var i = 0; i < task.getDepends().length; i++) {
        dep_string = '' + task.depends[i].name + ', ';
    }
//    row.find("[name=depends]").val(dep_string);
//    row.find(".taskResources").html(task.getResourcesString());

    //profiler.stop();
};


GridEditor.prototype.redraw = function () {
    for (var i = 0; i < this.master.tasks.length; i++) {
        this.refreshTaskRow(this.master.tasks[i]);
    }
};


GridEditor.prototype.reset = function () {
    this.element.find("[taskId]").remove();
};
