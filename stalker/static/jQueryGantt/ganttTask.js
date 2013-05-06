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
    this.build = function(kwargs){
    //    var start = kwargs['start'] || null;
    //    var duration = kwargs['duration'] || null;
        
        // Set at beginning of day
    //    var adjusted_start = computeStart(start);
          
    //    if (duration != null){
    //        var calculated_end = computeEndByDuration(adjusted_start, duration);
    //    } else {
    //        calculated_end = kwargs['end'];
    //    }
        
    //    kwargs['start'] = adjusted_start;
    //    kwargs['end'] = calculated_end;
        
        // copy computed date values if any
        kwargs['start'] = kwargs['computed_start'] || kwargs['start'];
        kwargs['end']   = kwargs['computed_end'] || kwargs['end'];
        
        return new Task(kwargs);
    };
}

function Task(kwargs) {
    this.id = kwargs['id'] || null;
    this.name = kwargs['name'] || null;
    this.code = kwargs['code'] || null;
    
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
    // schedule model:
    //   0: Effort
    //   1: Length
    //   2: Duration
    
    this.schedule_model = kwargs['schedule_model'];
    this.schedule_timing = kwargs['schedule_timing'] || 10;
    this.schedule_unit = kwargs['schedule_unit'] || 'h';
    this.schedule_constraint = kwargs['schedule_constraint'] || 0;
    
    this.schedule_seconds = kwargs['schedule_seconds'] || 0;
    this.total_logged_seconds = kwargs['total_logged_seconds'] || 0;
    
    
    this.bid_timing = kwargs['bid_timing'] || this.schedule_timing;
    this.bid_unit = kwargs['bid_unit'] || this.schedule_unit;
    
//    console.log('schedule_constraint : ', this.schedule_constraint);
//    console.log('schedule_model      : ', this.schedule_model);
//    console.log('schedule_timing     : ', this.schedule_timing);
//    console.log('schedule_unit       : ', this.schedule_unit);
//    console.log('bid_timing          : ', this.bid_timing);
//    console.log('bid_unit            : ', this.bid_unit);
    
    
    this.is_milestone = false;
    this.startIsMilestone = false;
    this.endIsMilestone = false;
    
    this.collapsed = false;
    
    this.rowElement; //row editor html element
    this.ganttElement; //gantt html element
    this.master;
    
    this.resources = kwargs['resources'] || [];
    this.resource_ids = [];
    for (var i=0; i<this.resources.length; i++){
      this.resource_ids.push(this.resources[i].id);
    }
    
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
  for (var i=0 ; i<this.resources.length ; i++) {
    var resource = this.resources[i];
    var res = this.master.getResource(resource.id);
    if (res) {
      ret = ret + (ret == "" ? "" : ", ") + res.name;
    }
  }
  return ret;
};

Task.prototype.getResourcesString_with_links = function () {
  var ret = "";
  for (var i=0 ; i<this.resources.length ; i++) {
    var resource = this.resources[i];
    var res = this.master.getResource(resource.id);
    if (res) {
      ret = ret + (ret == "" ? "" : ", ") + "<a class='DataLink' href='#' stalker_target='central_content' stalker_href='view/user/" + resource.id + "'>" + res.name + "</a>";
    }
  }
  return ret;
};

Task.prototype.link = function(){
    return "<a class='DataLink' href='#' stalker_target='tasks_content_pane' stalker_href='view/task/" + this.id + "'>" + this.name + "</a>";
};




Task.prototype.createResource = function (kwargs) {
  var resource = new Resource(kwargs);
  this.resources.push(resource);
  return resource;
};


//<%---------- SET PERIOD ---------------------- --%>
Task.prototype.setPeriod = function (start, end) {
    //console.debug("setPeriod ",this.name,new Date(start),new Date(end));
    //var profilerSetPer = new Profiler("gt_setPeriodJS");
    
    if (start instanceof Date) {
        start = start.getTime();
    }

    if (end instanceof Date) {
        end = end.getTime();
    }
    
    var originalPeriod = {
        start: this.start,
        end:  this.end,
        duration: this.duration,
        schedule_timing: this.schedule_timing
    };
    
    //console.debug("setStart",date,date instanceof Date);
    
    // round the values
    start = computeStart(start);
    end = computeEnd(end);
    
    var wantedStartMillis = start;
    
    //set a legal start
    //start = computeStart(start);

    //cannot start after end
    if (start > end) {
        start = end;
    }
    
    // update the schedule_timing
    // TODO: we need to consider the timing_resolution while doing this
    if (this.schedule_unit == 'h'){
        this.schedule_timing = (this.schedule_timing * (end - start) / (this.end - this.start)  >> 0);
    } else {
        this.schedule_timing = ((this.schedule_timing * (end - start) / (this.end - this.start) * 10) >> 0) / 10;
    }
    
    //if depends -> start is set to max end + lag of superior
    var sups = this.getSuperiors();
    if (sups && sups.length > 0){
        var supEnd = 0;
        var supTask;
        for (var i=0 ; i < sups.length ; i++) {
            supTask = sups[i];
            supEnd = Math.max(supEnd, supTask.end);
        }
        
        //if changed by depends move it
        if (computeStart(supEnd) > start) {
            return this.moveTo(supEnd + 1, false);
        }
    }
    
    var somethingChanged = false;
    
    if (this.start != start || this.start != wantedStartMillis) {
        this.start = start;
        somethingChanged = true;
    }
    
    //set end
    var wantedEndMillis = end;
    
    end = computeEnd(end);
//    end = start + originalPeriod.end - originalPeriod.start
    
    if (this.end != end || this.end != wantedEndMillis) {
        this.end = end;
        somethingChanged = true;
    }
    
    this.duration = recomputeDuration(this.start, this.end);
    
    //external dependencies: exit with error
    if (this.hasExternalDep) {
        this.master.setErrorOnTransaction(GanttMaster.messages["TASK_HAS_EXTERNAL_DEPS"] + "\n" + this.name, this);
        return false;
    }
    
    var todoOk = true;
    
    // if it has any children then set the start and end from children
    //loops children to get boundaries
    var children = this.getChildren();
    
    if (children.length > 0){
        var bs = Infinity;
        var be = 0;
        var child;
        for (var i = 0; i < children.length; i++) {
            child = children[i];
            be = Math.max(be, child.end);
            bs = Math.min(bs, child.start);
        }
        
        this.end = be;
        this.start = bs;
        
        this.duration = recomputeDuration(this.start, this.end);
    } else {
        //nothing changed exit
        if (!somethingChanged){
            return true;
        }
    }
    
    //check global boundaries
    if (this.start < this.master.minEditableDate || this.end > this.master.maxEditableDate) {
        this.master.setErrorOnTransaction(GanttMaster.messages["CHANGE_OUT_OF_SCOPE"], this);
        todoOk = false;
    }
    
    //console.debug("set period: somethingChanged",this);
    if (todoOk && !updateTree(this)) {
        todoOk = false;
    }
    
    if (todoOk) {
        //and now propagate to inferiors
        var infs = this.getInferiors();
        if (infs && infs.length > 0) {
            var link;
            for (var i=0 ; i<infs.length ; i++) {
                link = infs[i];
                todoOk = link.to.moveTo(end, false); //this is not the right date but moveTo checks start
                if (!todoOk)
                    break;
            }
        }
    }
    return todoOk;
};


//<%---------- MOVE TO ---------------------- --%>
Task.prototype.moveTo = function (start, ignoreMilestones) {
    //console.debug("moveTo ",this,start,ignoreMilestones);
    //var profiler = new Profiler("gt_task_moveTo");
    
    if (start instanceof Date) {
        start = start.getTime();
    }
    
    // update this.duration
    this.duration = this.end - this.start;
    
    var originalPeriod = {
        start: this.start,
        end: this.end
    };
    
    var wantedStartMillis = computeStart(start);
    
    //set a legal start
    start = wantedStartMillis;
    
    //if start is milestone cannot be move
    if (!ignoreMilestones && this.startIsMilestone && start != this.start) {
        //notify error
        this.master.setErrorOnTransaction(GanttMaster.messages["START_IS_MILESTONE"], this);
        return false;
    } else if (this.hasExternalDep) {
        //notify error
        this.master.setErrorOnTransaction(GanttMaster.messages["TASK_HAS_EXTERNAL_DEPS"], this);
        return false;
    }
    
    //if depends start is set to max end + lag of superior
    var sups = this.getSuperiors();
    if (sups && sups.length > 0) {
        var supEnd = 0;
        var link;
        for (var i=0 ; i < sups.length ; i++) {
            link = sups[i];
            supEnd = Math.max(supEnd, link.end);
        }
        if (supEnd > start){
            start = supEnd + 1;
        }
    }
    //set a legal start
    start = computeStart(start);
    
    var end = computeEndByDuration(start, this.duration);
    
    if (this.start != start || this.start != wantedStartMillis) {
        //in case of end is milestone it never changes, but recompute duration
        if (!ignoreMilestones && this.endIsMilestone) {
            end = this.end;
            this.duration = recomputeDuration(start, end);
        }
        this.start = start;
        this.end = end;
        //profiler.stop();
        
        //check global boundaries
        if (this.start < this.master.minEditableDate || this.end > this.master.maxEditableDate) {
            this.master.setErrorOnTransaction(GanttMaster.messages["CHANGE_OUT_OF_SCOPE"], this);
            return false;
        }
        
        var panDelta = originalPeriod.start - this.start;
        //console.debug("panDelta",panDelta);
        //loops children to shift them
        var children = this.getChildren();
        for (var i=0;i < children.length ; i++) {
            ch = children[i];
            if (!ch.moveTo(ch.start - panDelta, false)) {
                return false;
            }
        }
        
        //console.debug("set period: somethingChanged",this);
        if (!updateTree(this)) {
            return false;
        }
        
        //and now propagate to inferiors
        var infs = this.getInferiors();
        if (infs && infs.length > 0) {
            for (var i=0;i<infs.length;i++) {
                var link = infs[i];
                
                //this is not the right date but moveTo checks start
                if (!link.to.moveTo(end, false)) {
                    return false;
                }
            }
        }
    }

    return true;
};


function updateTree(task) {
    //console.debug("updateTree ",task);
    var error;
    
    //try to enlarge parent
    var p = task.getParent();
    
    //no parent:exit
    if (!p)
        return true;
    
    var newStart = p.start;
    var newEnd = p.end;
    
    if (p.start > task.start) {
        if (p.startIsMilestone) {
            task.master.setErrorOnTransaction(GanttMaster.messages["START_IS_MILESTONE"] + "\n" + p.name, task);
            return false;
        } else if (p.depends.length > 0) {
            task.master.setErrorOnTransaction(GanttMaster.messages["TASK_HAS_CONSTRAINTS"] + "\n" + p.name, task);
            return false;
        }
        newStart = task.start;
    }
    
    if (p.end < task.end) {
        if (p.endIsMilestone) {
            task.master.setErrorOnTransaction(GanttMaster.messages["END_IS_MILESTONE"] + "\n" + p.name, task);
            return false;
        }
        newEnd = task.end;
    }
    
    //propagate updates if needed
    if (p.hasExternalDep) {
        task.master.setErrorOnTransaction(GanttMaster.messages["TASK_HAS_EXTERNAL_DEPS"] + "\n" + p.name, task);
        return false;
    }
    
    // always propagate parent
    return p.setPeriod(newStart, newEnd);
}

//<%---------- CHANGE STATUS ---------------------- --%>
Task.prototype.changeStatus = function(newStatus) {
  //console.debug("changeStatus: "+this.name+" from "+this.status+" -> "+newStatus);
  //compute descendant for identify a cone where status changes propagate
  var cone = this.getDescendant();

  function propagateStatus(task, newStatus, manuallyChanged, propagateFromParent, propagateFromChildren) {
    var oldStatus = task.status;

    //no changes exit
    if(newStatus == oldStatus){
      return true;
    }
    //console.debug("propagateStatus: "+task.name + " from " + task.status + " to " + newStatus + " " + (manuallyChanged?" a manella":"")+(propagateFromParent?" da parent":"")+(propagateFromChildren?" da children":""));

    var todoOk = true;
    task.status = newStatus;

    //xxxx -> STATUS_DONE            may activate dependent tasks, both suspended and undefined. Will set to done all descendants.
    //STATUS_FAILED -> STATUS_DONE          do nothing if not forced by hand
    if (newStatus == "STATUS_DONE") {

      if ((manuallyChanged || oldStatus != "STATUS_FAILED")) { //cannot change for cascade when failed

        //can be closed only if superiors are already done
        var sups = task.getSuperiors();
        for (var i=0;i<sups.length;i++) {
          if (cone.indexOf(sups[i].from) < 0) {
            if (sups[i].from.status != "STATUS_DONE") {
              if (manuallyChanged || propagateFromParent)
                task.master.setErrorOnTransaction(GanttMaster.messages["GANTT_ERROR_DEPENDS_ON_OPEN_TASK"] + "\n" + sups[i].from.name + " -> " + task.name);
              todoOk = false;
              break;
            }
          }
        }

        if (todoOk) {
          var chds = task.getChildren();
          //set children as done
          for (var i=0;i<chds.length;i++)
            propagateStatus(chds[i], "STATUS_DONE", false,true,false);

          //set inferiors as active if outside the cone
          propagateToInferiors(cone, task.getInferiors(), "STATUS_ACTIVE");
        }
      } else {
        todoOk = false;
      }


      //  STATUS_UNDEFINED -> STATUS_ACTIVE       all children become active, if they have no dependencies.
      //  STATUS_SUSPENDED -> STATUS_ACTIVE       sets to active all children and their descendants that have no inhibiting dependencies.
      //  STATUS_DONE -> STATUS_ACTIVE            all those that have dependencies must be set to suspended.
      //  STATUS_FAILED -> STATUS_ACTIVE          nothing happens: child statuses must be reset by hand.
    } else if (newStatus == "STATUS_ACTIVE") {

      if ((manuallyChanged || oldStatus != "STATUS_FAILED")) { //cannot change for cascade when failed

        //activate parent if closed
        var par=task.getParent();
        if (par && par.status != "STATUS_ACTIVE") {
          todoOk=propagateStatus(par,"STATUS_ACTIVE",false,false,true);
        }

        if(todoOk){
          //can be active only if superiors are already done
          var sups = task.getSuperiors();
          for (var i=0;i<sups.length;i++) {
            if (sups[i].from.status != "STATUS_DONE") {
              if (manuallyChanged || propagateFromChildren)
              task.master.setErrorOnTransaction(GanttMaster.messages["GANTT_ERROR_DEPENDS_ON_OPEN_TASK"] + "\n" + sups[i].from.name + " -> " + task.name);
              todoOk = false;
              break;
            }
          }
        }

        if (todoOk) {
          var chds = task.getChildren();
          if (oldStatus == "STATUS_UNDEFINED" || oldStatus == "STATUS_SUSPENDED") {
            //set children as active
            for (var i=0;i<chds.length;i++)
              if (chds[i].status != "STATUS_DONE" )
                propagateStatus(chds[i], "STATUS_ACTIVE", false,true,false);
          }

          //set inferiors as suspended
          var infs = task.getInferiors();
          for (var i=0;i<infs.length;i++)
            propagateStatus(infs[i].to, "STATUS_SUSPENDED", false,false,false);
        }
      } else {
        todoOk = false;
      }

      // xxxx -> STATUS_SUSPENDED       all active children and their active descendants become suspended. when not failed or forced
      // xxxx -> STATUS_UNDEFINED       all active children and their active descendants become suspended. when not failed or forced
    } else if (newStatus == "STATUS_SUSPENDED" || newStatus == "STATUS_UNDEFINED") {
      if (manuallyChanged || oldStatus != "STATUS_FAILED") { //cannot change for cascade when failed

        //suspend parent if not active
        var par=task.getParent();
        if (par && par.status != "STATUS_ACTIVE") {
          todoOk=propagateStatus(par,newStatus,false,false,true);
        }


        var chds = task.getChildren();
        //set children as active
        for (var i=0;i<chds.length;i++){
          if (chds[i].status != "STATUS_DONE")
            propagateStatus(chds[i], newStatus, false,true,false);
        }

        //set inferiors as STATUS_SUSPENDED or STATUS_UNDEFINED
        propagateToInferiors(cone, task.getInferiors(), newStatus);
      } else {
        todoOk = false;
      }

      // xxxx -> STATUS_FAILED children and dependent failed
    } else if (newStatus == "STATUS_FAILED") {
      var chds = task.getChildren();
      //set children as failed
      for (var i=0;i<chds.length;i++)
        propagateStatus(chds[i], "STATUS_FAILED", false,true,false);

      //set inferiors as active
      //set children as done
      propagateToInferiors(cone, task.getInferiors(), "STATUS_FAILED");
    }
    if (!todoOk){
      task.status = oldStatus;
      //console.debug("status rolled back: "+task.name + " to " + oldStatus);
    }

    return todoOk;
  }

  /**
   * A helper method to traverse an array of 'inferior' tasks
   * and signal a status change.
   */
  function propagateToInferiors(cone, infs, status) {
    for (var i=0;i<infs.length;i++) {
      if (cone.indexOf(infs[i].to) < 0) {
        propagateStatus(infs[i].to, status, false, false, false);
      }
    }
  }

  var todoOk = true;
  var oldStatus = this.status;

  todoOk = propagateStatus(this, newStatus, true,false,false);

  if (!todoOk)
    this.status = oldStatus;

  return todoOk;
};

Task.prototype.synchronizeStatus=function(){
  var oldS = this.status;
  this.status = "";
  return this.changeStatus(oldS);
};

Task.prototype.isLocallyBlockedByDependencies=function(){
  var sups = this.getSuperiors();
  var blocked=false;
  for (var i=0 ; i<sups.length ; i++) {
    if (sups[i].from.status != "STATUS_DONE") {
      blocked=true;
      break;
    }
  }
  return blocked;
};

//<%---------- TASK STRUCTURE ---------------------- --%>
Task.prototype.getRow = function() {
  ret = -1;
  if (this.master)
    ret = this.master.tasks.indexOf(this);
  return ret;
};


Task.prototype.getParents = function() {
  var parents = [];
  var current_task = this.getParent();
  while(current_task != null){
    parents.push(current_task);
    current_task = current_task.parent;
  }
  return parents;
};


Task.prototype.getParent = function() {
  if (this.parent == null && this.parent_id != null){
    // there should be a parent
    // find the parent from parent_id
    var current_task;
    
    var parent_index = this.master.task_ids.indexOf(this.parent_id);
    if (parent_index != -1){
      this.parent = this.master.tasks[parent_index];
      // register the current task as a child of the parent task
      if (this.parent.children.indexOf(this)==-1){
          this.parent.children.push(this);
      }
    }
  }
  return this.parent;
};


Task.prototype.isParent = function(){
  return this.children.length > 0;
};


Task.prototype.getChildren = function() {
  return this.children;
};


Task.prototype.getDescendant = function() {
  return this.children;
};

Task.prototype.getDepends = function() {
    if (this.depends==null){
        this.depends = [];
        if (this.depend_ids.length > 0){
            // find the tasks
            var dep_id;
            var dep;
            var dep_index;
            for(var i=0; i < this.depend_ids.length; i++){
                dep_id = this.depend_ids[i];
                dep_index = this.master.task_ids.indexOf(dep_id);
                
                if (dep_index != -1){
                  dep = this.master.tasks[dep_index];
                  this.depends.push(dep);
                  // also update depends_string
                }
            }
        }
    }
    return this.depends;
};

Task.prototype.setDepends = function(depends){
    // if this is not an array but a string parse it as depends string
    var dependent_task;
    if (typeof(depends) == 'string'){
        // parse it as depends string
        this.depends_string = depends;
        this.depends = [];
        this.depend_ids = [];
        var deps = this.depends_string.split(',');
        var dep_id;
        var depend_index;
        for (var i=0; i < deps.length; i++){
            dep_id = deps[i].split(':')[0].trim(); // don't care about the lag
            depend_index = this.master.task_ids.indexOf(dep);
            if (depend_index != -1){
                dependent_task = this.master.tasks[depend_index];
                this.depends.push(dependent_task);
                this.depend_ids.push(dependent_task.id);
            }
        }
    } else if(depends instanceof Task) {
        // just set it to the depends list
        this.depends = [depends];
        this.depend_ids = [depends.id];
    } else if(depends instanceof Array) {
        // should be an array
        for (var i; i<depends.length ; i++){
            dependent_task = depends[i];
            if (dependent_task instanceof Task){
                this.depends.push(dependent_task);
                this.depend_ids.push(dependent_task.id);
            }
        }
    }
    // somebody should tell GanttMaster to update the links after this.
};



Task.prototype.getSuperiors = function() {
  // Returns the Tasks that this task depends to.
  
  //var ret = [];
  //var task = this;
  //if (this.master){
    //ret = this.master.links.filter(function(link) {
    //  return link.to == task;
    //});
  //}
  //return ret;
  return this.getDepends();
};


Task.prototype.getInferiors = function() {
    // Returns the tasks that depends to this task
    var ret = [];
    var task = this;
    if (this.master) {
      ret = this.master.links.filter(function(link) {
        return link.from == task;
      });
    }
    return ret;
};


Task.prototype.isNew = function(){
    return (this.id + "").indexOf("tmp_")==0;
};

Task.prototype.update_duration_from_schedule_timing = function(){
    // updates the duration from schedule_timing    
};


//<%------------------------------------------------------------------------  LINKS OBJECT ---------------------------------------------------------------%>
function Link(taskFrom, taskTo, lagInWorkingDays) {
    this.from = taskFrom;
    this.to = taskTo;
    this.lag = lagInWorkingDays;
}


//<%------------------------------------------------------------------------  RESOURCE ---------------------------------------------------------------%>
function Resource(kwargs) {
    this.id = kwargs['id'] || null;
    this.name = kwargs['name'] || (this.id || '');
}

