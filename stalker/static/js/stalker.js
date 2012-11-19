
require(["dijit/registry", "dojox/widget/DialogSimple", "dijit/form/Button"],
    function(registry, DialogSimple, Button){
        
        // ********************************************************************
        // ADD DATA BUTTON
        // TODO: what is parent and what is dialog_id
        create_add_data_button = function(
            parent,
            label,
            dialog_id,
            content_creator,
            dom_element
            ){
            // parent: The parent widget, null if there are no parents defined
            // label: The label of the add button
            // dialog_id: the id of the parent dialog
            // dialog_creator: the content creator function for the dialog
            // dom_element: the dom element to attach this button to
            return new Button({
                label: label,
                type: 'Button',
                onClick: function(){
                    // create the dialog if it doesn't already exists
                    var dialog = dijit.byId(dialog_id);
                    if (dialog == null){
                        dialog = content_creator(parent);
                    }
                    // show the dialog
                    dialog.show();
                }
            }, dom_element);
        };
        
        // ********************************************************************
        // EDIT DATA BUTTON
        create_edit_data_button = function(
            parent,
            label,
            dialog_id,
            content_creator,
            dom_element,
            edited_data_id_getter
            ){
            // parent: The parent widget, null if there are no parents defined
            // label: The label of the add button
            // dialog_id: The id of the parent dialog
            return new Button({
                label: label,
                type: 'Button',
                onClick: function(){
                    // create the dialog and pass the data in to it
                    var dialog = dijit.byId(dialog_id);
                    if (dialog == null){
                        dialog = content_creator(parent, edited_data_id_getter());
                    }
                    
                    alert(dialog);
                    alert(parent);
                    
                    // show the dialog
                    dialog.show();
                }
            }, dom_element)
        };
        
        
        // ********************************************************************
        // PROJECT
        create_add_project_dialog = function (parent){
            // create the dialog
            var myDialog = new DialogSimple({
                id: 'add_project_dialog',
                title: 'Add Project',
                href: '/add/project',
                style: "width: 380px; height auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        
        // ********************************************************************
        // IMAGE FORMAT
        create_add_image_format_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_image_format_dialog',
                title: 'Add Image Format',
                href: '/add/image_format',
                resize: true,
                style: "width: 380px; height auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_image_format_dialog = function(parent, image_format_id){
            var myDialog = new DialogSimple({
                id: 'edit_image_format_dialog',
                title: 'Edit Image Format',
                href: '/edit/image_format/' + image_format_id,
                resize: true,
                style: "width: 380px; height: auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        // ********************************************************************
        // STRUCTURE
        create_add_structure_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_structure_dialog',
                title: 'Add Structure',
                href: '/add/structure',
                resize: true,
                style: "width: 380px; height: auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_structure_dialog = function(parent, structure_id){
            var myDialog = new DialogSimple({
                id: 'edit_structure_dialog',
                title: 'Edit Structure',
                href: '/edit/structure/' + structure_id,
                resize: true,
                style: "width: 380px; height: auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        // ********************************************************************
        // USER
        create_add_user_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_user_dialog',
                title: 'Add User',
                href: '/add/user',
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_user_dialog = function(parent, user_id){
            var myDialog = new DialogSimple({
                id: 'edit_user_dialog',
                title: 'Edit User',
                href: 'edit/user/' + user_id,
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        

        // ********************************************************************
        // FILENAME TEMPLATE
        create_add_filename_template_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_filename_template_dialog',
                title: 'Add Filename Template',
                href: '/add/filename_template',
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_filename_template_dialog = function(parent,
                                                        filename_template_id){
            var myDialog = new DialogSimple({
                id: 'edit_filename_template_dialog',
                title: 'Edit Filename Template',
                href: 'edit/filename_template/' + filename_template_id,
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
         
        // ********************************************************************
        // REPOSITORY
        create_add_repository_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_repository_dialog',
                title: 'Add Repository',
                href: '/add/repository',
                resize: true,
                style: "width: 380px; height auto; padding: 0px",
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_repository_dialog = function(parent, repo_id){
            var myDialog = new DialogSimple({
                id: 'edit_repository_dialog',
                title: 'Edit Repository',
                href: '/edit/repository/' + repo_id,
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        // ********************************************************************
        // STATUS LIST
        create_add_status_list_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_status_list_dialog',
                title: 'Add Status List',
                href: '/add/status_list',
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_status_list_dialog = function(parent, status_list_id){
            var myDialog = new DialogSimple({
                id: 'edit_status_list_dialog',
                title: 'Edit Status List',
                href: '/edit/status_list/' + status_list_id,
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        // ********************************************************************
        // STATUS
        create_add_status_dialog = function(parent){
            var myDialog = new DialogSimple({
                id: 'add_status_dialog',
                title: 'Add Status',
                href: '/add/status',
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
        
        create_edit_status_dialog = function(parent, status_id){
            var myDialog = new DialogSimple({
                id: 'edit_status_dialog',
                title: 'Edit Status',
                href: '/edit/status/' + status_id,
                resize: true,
                style: 'width: 380px; height: auto; padding: 0px',
                executeScripts: true
            });
            myDialog.set('parent', parent);
            return myDialog;
        };
 });

