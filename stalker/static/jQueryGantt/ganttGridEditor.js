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


GridEditor.prototype.fillEmptyLines = function() {
  var factory = new TaskFactory();

  //console.debug("GridEditor.fillEmptyLines");
  var rowsToAdd = 30 - this.element.find(".taskEditRow").size();
  
  //fill with empty lines
  for (var i = 0; i < rowsToAdd; i++) {
    var emptyRow = $.JST.createFromTemplate({}, "TASKEMPTYROW");
    //click on empty row create a task and fill above
    this.element.append(emptyRow);
  }
};


GridEditor.prototype.addTask = function(task, row) {
  //console.debug("GridEditor.addTask",task,row);
  //var prof = new Profiler("editorAddTaskHtml");

  //remove extisting row
  this.element.find("[taskId=" + task.id + "]").remove();

  var taskRow = $.JST.createFromTemplate(task, "TASKROW");
  //save row element on task
  task.rowElement = taskRow;

  this.bindRowEvents(task, taskRow);

  if (typeof(row) != "number") {
    var emptyRow = this.element.find(".emptyRow:first"); //tries to fill an empty row
    if (emptyRow.size() > 0)
      emptyRow.replaceWith(taskRow);
    else
      this.element.append(taskRow);
  } else {
    var tr = this.element.find("tr.taskEditRow").eq(row);
    if (tr.size() > 0) {
      tr.before(taskRow);
    } else {
      this.element.append(taskRow);
    }

  }
  this.element.find(".taskRowIndex").each(function(i, el) {
    $(el).html(i + 1);
  });
  //prof.stop();

  return taskRow;
};


GridEditor.prototype.refreshTaskRow = function(task) {
    //console.debug("refreshTaskRow")
    //var profiler = new Profiler("editorRefreshTaskRow");
    var row = task.rowElement;
    
    row.find(".taskRowIndex").html(task.getRow() + 1);
    row.find(".indentCell").css("padding-left", task.getParents().length * 10);
    row.find("[name=name]").val(task.name);
    row.find("[name=code]").val(task.code);
    row.find("[status]").attr("status", task.status);
    
    row.find("[name=duration]").val(task.duration);
    row.find("[name=start]").val(new Date(task.start).format()).updateOldValue(); // called on dates only because for other field is called on focus event
    row.find("[name=end]").val(new Date(task.end).format()).updateOldValue();
    
    var dep_string = '';
    for (var i; i < task.getDepends().length ; i++){
        dep_string = '' + task.depends[i] + ', ';
    }
    row.find("[name=depends]").val(dep_string);
    row.find(".taskResources").html(task.getResourcesString());

    //profiler.stop();
};

GridEditor.prototype.redraw = function() {
  for (var i = 0; i < this.master.tasks.length; i++) {
    this.refreshTaskRow(this.master.tasks[i]);
  }
};

GridEditor.prototype.reset = function() {
  this.element.find("[taskId]").remove();
};


GridEditor.prototype.bindRowEvents = function (task, taskRow) {
  var self = this;
  //console.debug("bindRowEvents",this,this.master,this.master.canWrite);
  if (this.master.canWrite) {
    self.bindRowInputEvents(task,taskRow);

  } else { //cannot write: disable input
    taskRow.find("input").attr("readonly", true);
  }

  //taskRow.find(".edit").click(function() {self.openFullEditor(task,taskRow)});

};


GridEditor.prototype.bindRowInputEvents = function (task, taskRow) {
  var self = this;

  //bind dateField on dates
//  taskRow.find(".date").each(function () {
//    var el = $(this);
//    
//    el.click(function () {
//      var inp = $(this);
//      inp.dateField({
//        inputField:el
//      });
//    });
//
//    el.blur(function (date) {
//      var inp = $(this);
//      if (inp.isValueChanged()) {
//        if (!Date.isValid(inp.val())) {
//          alert(GanttMaster.messages["INVALID_DATE_FORMAT"]);
//          inp.val(inp.getOldValue());
//
//        } else {
//          var date = Date.parseString(inp.val());
//          var row = inp.closest("tr");
//          var taskId = row.attr("taskId");
//          var task = self.master.getTask(taskId);
//          var lstart = task.start;
//          var lend = task.end;
//
//          if (inp.attr("name") == "start") {
//            lstart = date.getTime();
//            if (lstart >= lend) {
//              var end_as_date = new Date(lstart);
//              lend = end_as_date.add('d', task.duration).getTime();
//            }
//
//            //update task from editor
//            self.master.beginTransaction();
//            self.master.moveTask(task, lstart);
//            self.master.endTransaction();
//
//          } else {
//            var end_as_date = new Date(date.getTime());
//            lend = end_as_date.getTime();
//            if (lstart >= lend) {
//              end_as_date.add('d', -1 * task.duration);
//              lstart = end_as_date.getTime();
//            }
//
//            //update task from editor
//            self.master.beginTransaction();
//            self.master.changeTaskDates(task, lstart, lend);
//            self.master.endTransaction();
//          }
//
//
//          inp.updateOldValue(); //in order to avoid multiple call if nothing changed
//        }
//      }
//    });
//  });


//  //binding on blur for task update (date exluded as click on calendar blur and then focus, so will always return false, its called refreshing the task row)
//  taskRow.find("input:not(.date)").focus(function () {
//    $(this).updateOldValue();
//
//  }).blur(function () {
//    var el = $(this);
//    if (el.isValueChanged()) {
//      var row = el.closest("tr");
//      var taskId = row.attr("taskId");
//
//      var task = self.master.getTask(taskId);
//
//      //update task from editor
//      var field = el.attr("name");
//
//      self.master.beginTransaction();
//
//      if (field == "depends") {
//        task.setDepends(el.val()); // set the depends with the depends_string
//        // update links
//        var linkOK = self.master.updateLinks(task);
//        if (linkOK) {
//          //synchronize status fro superiors states
//          var sups = task.getSuperiors();
//          for (var i = 0; i < sups.length; i++) {
//            if (!sups[i].from.synchronizeStatus())
//              break;
//          }
//
//          self.master.changeTaskDates(task, task.start, task.end);
//        }
//
//      } else if (field == "duration") {
//        var dur = task.duration;
//        dur = parseInt(el.val()) || 1;
//        el.val(dur);
//        var newEnd = computeEndByDuration(task.start, dur);
//        self.master.changeTaskDates(task, task.start, newEnd);
//
//      } else {
//        task[field] = el.val();
//      }
//      self.master.endTransaction();
//    }
//  });


//  //change status
//  taskRow.find(".taskStatus").click(function () {
//    var el = $(this);
//    var tr = el.closest("[taskId]");
//    var taskId = tr.attr("taskId");
//    var task = self.master.getTask(taskId);
//
//    var changer = $.JST.createFromTemplate({}, "CHANGE_STATUS");
//    changer.css("top", tr.position().top + self.element.parent().scrollTop());
//    changer.find("[status=" + task.status + "]").addClass("selected");
//    changer.find(".taskStatus").click(function () {
//      self.master.beginTransaction();
//      task.changeStatus($(this).attr("status"));
//      self.master.endTransaction();
//      el.attr("status", task.status);
//      changer.remove();
//      el.show();
//
//    });
//    el.hide().oneTime(3000, "hideChanger", function () {
//      changer.remove();
//      $(this).show();
//    });
//    el.after(changer);
//  });


  ////expand collapse todo to be completed
  //taskRow.find(".expcoll").click(function(){
  //  //expand?
  //  var el=$(this);
  //  var taskId=el.closest("[taskId]").attr("taskId");
  //  var task=self.master.getTask(taskId);
  //  var descs=task.getDescendant();
  //  if (el.is(".exp")){
  //    for (var i=0;i<descs.length;i++)
  //      descs[i].rowElement.show();
  //  } else {
  //    for (var i=0;i<descs.length;i++)
  //      descs[i].rowElement.hide();
  //  }
  //});

  //bind row selection
  taskRow.click(function () {
    var row = $(this);
    //var isSel = row.hasClass("rowSelected");
    row.closest("table").find(".rowSelected").removeClass("rowSelected");
    row.addClass("rowSelected");
    
    //set current task
    self.master.currentTask = self.master.getTask(row.attr("taskId"));
    
    //move highlighter
    if (self.master.currentTask.ganttElement)
      self.master.gantt.highlightBar.css("top", self.master.currentTask.ganttElement.position().top);
    
    //if offscreen scroll to element
    var top = row.position().top;
    if (row.position().top > self.element.parent().height()) {
      self.master.gantt.element.parent().scrollTop(row.position().top - self.element.parent().height() + 100);
    }
  });

};


