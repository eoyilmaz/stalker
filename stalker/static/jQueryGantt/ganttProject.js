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


function Project(kwargs){
    this.id = kwargs['id'] || null;
    this.code = kwargs['code'] || code;
    this.name = kwargs['name'] || name;
    
    this.start = kwargs['start'] || null;
    this.duration = kwargs['duration'] || null;
    this.end = kwargs['end'] || null;    
    
    this.task_ids = [];
    this.tasks = [];
    
    
    this.rowElement; //row editor html element
    this.ganttElement; //gantt html element
    this.master;
}

Project.prototype.clone = function () {
  var ret = {};
  for (var key in this) {
    if (typeof(this[key]) != "function") {
      ret[key] = this[key];
    }
  }
  return ret;
};

Project.prototype.link = function(){
    return "<a class='DataLink' href='#' stalker_target='central_pane' stalker_href='view/project/" + this.id + "'>" + this.name + "</a>";
};


//<%---------- PROJECT STRUCTURE ---------------------- --%>
Project.prototype.getRow = function() {
  ret = -1;
  if (this.master)
    ret = this.master.projects.indexOf(this);
  return ret;
};
