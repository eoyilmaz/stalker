require(['dijit/registry', 'dojo/_base/lang','dojo/request/xhr',
    'dojo/store/Memory', 'dojox/widget/DialogSimple', 'dojo/ready'],
    function(registry, lang, xhr, Memory, DialogSimple, ready){
        
        var style = 'width: auto; height: auto; padding: 0px;';
        
        // ********************************************************************
        // PROJECT
        create_create_project_dialog = function (){
                return new DialogSimple({
                    id: 'create_project_dialog',
                    title: 'New Project',
                    href: '/create/project',
                    resize: true,
                    style: style,
                    executeScripts: true
                });
            
        };
        
        create_update_project_dialog = function(project_id){
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
        create_create_image_format_dialog = function(){
            return new DialogSimple({
                id: 'create_image_format_dialog',
                title: 'New Image Format',
                href: '/create/image_format',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_image_format_dialog = function(image_format_id){
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
        create_create_structure_dialog = function(){
            return new DialogSimple({
                id: 'create_structure_dialog',
                title: 'New Structure',
                href: '/create/structure',
                resize: true,
                style: style,
                executeScripts: true
            }); 
        };
        
        create_update_structure_dialog = function(structure_id){
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
        create_create_user_dialog = function(department_id){
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
        
        create_update_user_dialog = function(user_id){
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
        create_create_filename_template_dialog = function(){
            return new DialogSimple({
                id: 'create_filename_template_dialog',
                title: 'New Filename Template',
                href: '/create/filename_template',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_filename_template_dialog = function(filename_template_id){
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
        create_create_repository_dialog = function(){
            return new DialogSimple({
                id: 'create_repository_dialog',
                title: 'New Repository',
                href: '/create/repository',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_repository_dialog = function(repo_id){
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
        create_create_status_list_dialog = function(target_entity_type){
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
        
        create_update_status_list_dialog = function(status_list_id){
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
        create_create_status_dialog = function(){
            return new DialogSimple({
                id: 'create_status_dialog',
                title: 'New Status',
                href: '/create/status',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_status_dialog = function(status_id){
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
        create_create_asset_dialog = function(project_id){
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
        create_create_shot_dialog = function(project_id){
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
        
        create_update_shot_dialog = function(shot_id){
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
        create_create_sequence_dialog = function(project_id){
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
        
        create_update_sequence_dialog = function(sequence_id){
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
        create_create_task_dialog = function(taskable_entity_id){
            return new DialogSimple({
                id: 'create_task_dialog',
                title: 'New Task',
                href: '/create/task/' + taskable_entity_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_task_dialog = function(task_id){
            return new DialogSimple({
                id: 'update_task_dialog',
                title: 'Update Task',
                href: '/update/task/' + task_id,
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        // ********************************************************************
        // DEPARTMENT
        create_create_department_dialog = function(){
            return new DialogSimple({
                id: 'create_department_dialog',
                title: 'New Department',
                href: '/create/department',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_department_dialog = function(department_id){
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
        create_create_group_dialog = function(){
            return new DialogSimple({
                id: 'create_group_dialog',
                title: 'New Group',
                href: '/create/group',
                resize: true,
                style: style,
                executeScripts: true
            });
        };
        
        create_update_group_dialog = function(group_id){
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

