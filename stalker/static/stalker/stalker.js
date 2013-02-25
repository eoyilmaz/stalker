require(['dijit/registry', 'dojo/_base/lang','dojo/request/xhr',
    'dojo/store/Memory', 'dojox/widget/DialogSimple'],
    function(registry, lang, xhr, Memory, DialogSimple){
        
        var style = 'width: auto; height: auto; padding: 0px;';
        
        // ********************************************************************
        // PROJECT
        create_add_project_dialog = function (){
            return new DialogSimple({
                id: 'add_project_dialog',
                title: 'Add Project',
                href: '/add/project',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_project_dialog = function(project_id){
            return new DialogSimple({
                id: 'edit_project_dialog',
                title: 'Edit Project',
                href: '/edit/project/' + project_id,
                resize: true,
                style: style,
                executeScripts: true
            })
        };
        
        // ********************************************************************
        // IMAGE FORMAT
        create_add_image_format_dialog = function(){
            return new DialogSimple({
                id: 'add_image_format_dialog',
                title: 'Add Image Format',
                href: '/add/image_format',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_image_format_dialog = function(image_format_id){
            return new DialogSimple({
                id: 'edit_image_format_dialog',
                title: 'Edit Image Format',
                href: '/edit/image_format/' + image_format_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STRUCTURE
        create_add_structure_dialog = function(){
            return new DialogSimple({
                id: 'add_structure_dialog',
                title: 'Add Structure',
                href: '/add/structure',
                resize: true,
                style: style,
                executeScripts: true
            }); 
        };
        
        create_edit_structure_dialog = function(structure_id){
            return new DialogSimple({
                id: 'edit_structure_dialog',
                title: 'Edit Structure',
                href: '/edit/structure/' + structure_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // USER
        create_add_user_dialog = function(){
            return new DialogSimple({
                id: 'add_user_dialog',
                title: 'Add User',
                href: '/add/user',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_user_dialog = function(user_id){
            var myDialog = new DialogSimple({
                id: 'edit_user_dialog',
                title: 'Edit User',
                href: 'edit/user/' + user_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // FILENAME TEMPLATE
        create_add_filename_template_dialog = function(){
            return new DialogSimple({
                id: 'add_filename_template_dialog',
                title: 'Add Filename Template',
                href: '/add/filename_template',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_filename_template_dialog = function(filename_template_id){
            var myDialog = new DialogSimple({
                id: 'edit_filename_template_dialog',
                title: 'Edit Filename Template',
                href: 'edit/filename_template/' + filename_template_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
         
        // ********************************************************************
        // REPOSITORY
        create_add_repository_dialog = function(){
            return new DialogSimple({
                id: 'add_repository_dialog',
                title: 'Add Repository',
                href: '/add/repository',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_repository_dialog = function(repo_id){
            return new DialogSimple({
                id: 'edit_repository_dialog',
                title: 'Edit Repository',
                href: '/edit/repository/' + repo_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STATUS LIST
        create_add_status_list_dialog = function(target_entity_type){
            var href;
            if (target_entity_type == null){
                href = '/add/status_list'
            } else {
                href = '/add/status_list/' + target_entity_type
            }
            return new DialogSimple({
                id: 'add_status_list_dialog',
                title: 'Add Status List',
                href: href,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_status_list_dialog = function(status_list_id){
            return new DialogSimple({
                id: 'edit_status_list_dialog',
                title: 'Edit Status List',
                href: '/edit/status_list/' + status_list_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // STATUS
        create_add_status_dialog = function(){
            return new DialogSimple({
                id: 'add_status_dialog',
                title: 'Add Status',
                href: '/add/status',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_status_dialog = function(status_id){
            return new DialogSimple({
                id: 'edit_status_dialog',
                title: 'Edit Status',
                href: '/edit/status/' + status_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // ASSET
        create_add_asset_dialog = function(){
            return new DialogSimple({
                id: 'add_asset_dialog',
                title: 'Add Asset',
                href: '/add/asset',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // SHOT
        create_add_shot_dialog = function(){
            return new DialogSimple({
                id: 'add_shot_dialog',
                title: 'Add Shot',
                href: '/add/shot',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_shot_dialog = function(shot_id){
            return new DialogSimple({
                id: 'edit_shot_dialog',
                title: 'Edit Shot',
                href: '/edit/shot/' + shot_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // SEQUENCE
        create_add_sequence_dialog = function(){
            return new DialogSimple({
                id: 'add_sequence_dialog',
                title: 'Add Sequence',
                href: '/add/sequence',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_sequence_dialog = function(sequence_id){
            return new DialogSimple({
                id: 'edit_sequence_dialog',
                title: 'Edit Sequence',
                href: '/edit/sequence/' + sequence_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // TASK
        create_add_task_dialog = function(taskable_entity_id){
            return new DialogSimple({
                id: 'add_task_dialog',
                title: 'Add Task',
                href: '/add/task/' + taskable_entity_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_task_dialog = function(task_id){
            return new DialogSimple({
                id: 'edit_task_dialog',
                title: 'Edit Task',
                href: '/edit/task/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // DEPARTMENT
        create_add_department_dialog = function(){
            return new DialogSimple({
                id: 'add_department_dialog',
                title: 'Add Department',
                href: '/add/department',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_department_dialog = function(department_id){
            return new DialogSimple({
                id: 'edit_department_dialog',
                title: 'Edit Department',
                href: '/edit/department/' + department_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // GROUPS
        create_add_group_dialog = function(){
            return new DialogSimple({
                id: 'add_group_dialog',
                title: 'Add Group',
                href: '/add/group',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_edit_group_dialog = function(group_id){
            return new DialogSimple({
                id: 'edit_group_dialog',
                title: 'Edit Group',
                href: '/edit/group/' + group_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
});

