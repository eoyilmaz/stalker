// Stalker a Production Asset Management System
// Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
//
// This file is part of Stalker.
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

require(['dijit/registry', 'dojo/_base/lang','dojo/request/xhr',
    'dojo/store/Memory', 'dojox/widget/DialogSimple', 'dojo/ready'],
    function(registry, lang, xhr, Memory, DialogSimple, ready){
        
        var style = 'width: auto; height: auto; padding: 0px;';
        
        // ********************************************************************
        // PROJECT
        create_project_dialog_creator = function (){
                return new DialogSimple({
                    id: 'create_project_dialog',
                    title: 'New Project',
                    href: '/create/project',
                    resize: true,
                    style: style,
                    executeScripts: true
                });
            
        };
        
        update_project_dialog_creator = function(project_id){
            return new DialogSimple({
                id: 'update_project_dialog',
                title: 'Update Project',
                href: '/update/project/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            })
        };
        
        // ********************************************************************
        // IMAGE FORMAT
        create_image_format_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_image_format_dialog',
                title: 'New Image Format',
                href: '/create/image_format',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_image_format_dialog_creator = function(image_format_id){
            return new DialogSimple({
                id: 'update_image_format_dialog',
                title: 'Update Image Format',
                href: '/update/image_format/' + image_format_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STRUCTURE
        create_structure_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_structure_dialog',
                title: 'New Structure',
                href: '/create/structure',
                resize: true,
                style: style,
                executeScripts: true
            }); 
        };
        
        update_structure_dialog_creator = function(structure_id){
            return new DialogSimple({
                id: 'update_structure_dialog',
                title: 'Update Structure',
                href: '/update/structure/' + structure_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // USER
        create_user_dialog_creator = function(department_id){
            department_id = department_id || -1;
            return new DialogSimple({
                id: 'create_user_dialog',
                title: 'New User',
                href: '/create/user/' + department_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_user_dialog_creator = function(user_id){
            var myDialog = new DialogSimple({
                id: 'update_user_dialog',
                title: 'Update User',
                href: 'update/user/' + user_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // FILENAME TEMPLATE
        create_filename_template_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_filename_template_dialog',
                title: 'New Filename Template',
                href: '/create/filename_template',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_filename_template_dialog_creator = function(filename_template_id){
            var myDialog = new DialogSimple({
                id: 'update_filename_template_dialog',
                title: 'Update Filename Template',
                href: 'update/filename_template/' + filename_template_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
         
        // ********************************************************************
        // REPOSITORY
        create_repository_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_repository_dialog',
                title: 'New Repository',
                href: '/create/repository',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_repository_dialog_creator = function(repo_id){
            return new DialogSimple({
                id: 'update_repository_dialog',
                title: 'Update Repository',
                href: '/update/repository/' + repo_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STATUS LIST
        create_status_list_dialog_creator = function(target_entity_type){
            var href;
            if (target_entity_type == null){
                href = '/create/status_list'
            } else {
                href = '/create/status_list/' + target_entity_type
            }
            return new DialogSimple({
                id: 'create_status_list_dialog',
                title: 'New Status List',
                href: href,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_status_list_dialog_creator = function(status_list_id){
            return new DialogSimple({
                id: 'update_status_list_dialog',
                title: 'Update Status List',
                href: '/update/status_list/' + status_list_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STATUS
        create_status_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_status_dialog',
                title: 'New Status',
                href: '/create/status',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_status_dialog_creator = function(status_id){
            return new DialogSimple({
                id: 'update_status_dialog',
                title: 'Update Status',
                href: '/update/status/' + status_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // ASSET
        create_asset_dialog_creator = function(project_id){
            project_id = project_id || -1;
            return new DialogSimple({
                id: 'create_asset_dialog',
                title: 'New Asset',
                href: '/create/asset/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // SHOT
        create_shot_dialog_creator = function(project_id){
            project_id = project_id || -1;
            return new DialogSimple({
                id: 'create_shot_dialog',
                title: 'New Shot',
                href: '/create/shot/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_shot_dialog_creator = function(shot_id){
            return new DialogSimple({
                id: 'update_shot_dialog',
                title: 'Update Shot',
                href: '/update/shot/' + shot_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // SEQUENCE
        create_sequence_dialog_creator = function(project_id){
            project_id = project_id || -1;
            return new DialogSimple({
                id: 'create_sequence_dialog',
                title: 'New Sequence',
                href: '/create/sequence/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_sequence_dialog_creator = function(sequence_id){
            return new DialogSimple({
                id: 'update_sequence_dialog',
                title: 'Update Sequence',
                href: '/update/sequence/' + sequence_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // TASK
        create_task_dialog_creator = function(project_id){
            return new DialogSimple({
                id: 'create_task_dialog',
                title: 'New Task',
                href: 'dialog/create/task/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_task_dialog_creator = function(task_id){
            return new DialogSimple({
                id: 'update_task_dialog',
                title: 'Update Task',
                href: '/update/task/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_child_task_dialog_creator = function(task_id){
            return new DialogSimple({
                id: 'create_task_dialog',
                title: 'New Child Task',
                href: '/dialog/create/child_task/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_dependent_task_dialog_creator = function(task_id){
            return new DialogSimple({
                id: 'create_task_dialog',
                title: 'New Dependent Task',
                href: '/dialog/create/dependent_task/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // BOOKING
        create_booking_dialog_creator = function(task_id){
            return new DialogSimple({
                id: 'create_booking_dialog',
                title: 'New Booking',
                href: 'dialog/create/booking/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_booking_dialog_creator = function(booking_id){
            return new DialogSimple({
                id: 'update_booking_dialog',
                title: 'Update Booking',
                href: 'dialog/update/booking/' + booking_id,
                resize: true,
                style: style,
                executeScripts: true
            })
        };
        
        // ********************************************************************
        // DEPARTMENT
        create_department_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_department_dialog',
                title: 'New Department',
                href: '/create/department',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_department_dialog_creator = function(department_id){
            return new DialogSimple({
                id: 'update_department_dialog',
                title: 'Update Department',
                href: '/update/department/' + department_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // GROUPS
        create_group_dialog_creator = function(){
            return new DialogSimple({
                id: 'create_group_dialog',
                title: 'New Group',
                href: '/create/group',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        update_group_dialog_creator = function(group_id){
            return new DialogSimple({
                id: 'update_group_dialog',
                title: 'Update Group',
                href: '/update/group/' + group_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
});

