require(['dijit/registry', 'dojo/_base/lang','dojo/request/xhr',
    'dojo/store/Memory', 'dojox/widget/DialogSimple', 'dijit/form/Button',
    'dojo/_base/fx', 'dijit/MenuItem'],
    function(registry, lang, xhr, Memory, DialogSimple, Button, fx, MenuItem){
        
        // ********************************************************************
        // FIELD_UPDATER
        // 
        // Returns a function which when called updates a field
        //
        // memory: dojo.store.JsonRest
        //  the JsonRest instance
        // 
        // widget: dojo._WidgetBase
        //  the widget to update the data to
        //
        // query_data: String or function
        //  the data to be queried to, Anonymous functions are accepted
        // 
        // selected: Array
        //  stores what is selected among the data
        // 
        field_updater = function(kwargs){
            var memory = kwargs.memory;
            var widget = kwargs.widget;
            var query_data = kwargs.query_data || null;
            var selected = kwargs.selected || [];
            
            return function(){
                var animate = arguments[0] || true;
                var query;
                
                if (query_data != null){
                    var data_id;
                    if (typeof(query_data) == 'function'){
                        data_id = query_data();
                    } else {
                        data_id = query_data;
                    }
                    
                    if (data_id == ''){
                        return;
                    }
                    
                    query = memory.query(data_id);
                } else {
                    query = memory.query();
                }
                
                var result = query.then(function(data){
                    
                    // if the widget is a MultiSelect
                    if (widget.declaredClass == "dijit.form.MultiSelect"){
                        widget.reset();
                        // add options manually
                        // remove the previous options first
                        dojo.query('option', widget.domNode).forEach(function(opt, idx, arr){
                            dojo.destroy(opt);
                        });
                        
                        // add options
                        for (var i=0; i < data.length; i++){
                            dojo.create(
                                'option',
                                {
                                    'value': data[i].id,
                                    'innerHTML': data[i].name
                                },
                                widget.domNode
                            );
                        }
                        
                        // select selected
                        if (selected.length){
                            widget.setValue(selected);
                        }
                    } else if (widget.declaredClass == 'dojox.grid.DataGrid') {
                        // just call render
                        widget.render();
                    } else {
                        widget.reset();
                        // set the data normally
                        widget.set('store', new Memory({data: data}));
                        if (data.length > 0){
                            widget.attr('value', data[0].id);
                        }
                    }
                    
                    if (animate == true){
                        // animate the field to indicate it is updated
                        var domNode = widget.domNode;
                        fx.animateProperty({
                            node: domNode,
                            duration: 500,
                            properties: {
                                backgroundColor: {  
                                    start: "#00ff00",
                                    end: "white"
                                }
                            }
                        }).play();
                    }
                });
            };
        };
        
        // ********************************************************************
        // CREATE ADD EDIT DATA WIDGET
        //
        // Creates a widget (a button or a menuItem) to add/edit some data
        // depending on to the given dialog.
        // 
        // PARAMETERS
        // 
        // label:
        //   The label of the widget, default is 'Add'
        // 
        // dialog_id:
        //   the id of the parent dialog
        // 
        // content_creator:
        //   the content creator function for the dialog
        // 
        // attach_to:
        //   the dom element to attach this button to
        // 
        // data_id:
        //   if we already have some id for the data, let say if we are adding
        //   a new Sequence to a Project then this is the id or a function that
        //   returns the Project.id or if we are editing a data then this is
        //   the id or a function returning the edited data id (ex:
        //   sequence_id).
        //   
        //   If the id of the edited data is not yet known you can pass a
        //   function that will return the data id.
        //
        // related_field_updater:
        //   a function object without any parameters which will update the
        //   the related field which this form is adding data to.
        // 
        // widget_type: 'Button' or 'MenuItem'
        //   the type of widget
        // 
        create_add_edit_data_widget = function(kwargs){
            var label = kwargs.label || 'Add';
            var dialog_id = kwargs.dialog_id || null;
            var content_creator = kwargs.content_creator;
            var attach_to = kwargs.attach_to;
            var data_id = kwargs.data_id || function(){};
            var related_field_updater = kwargs.related_field_updater || function(){};
            var widget_type = kwargs.widget_type || 'Button';
            
            var WidgetClass = Button;
            if (widget_type == 'MenuItem'){
                WidgetClass = MenuItem;
            }
            
            var widget = new WidgetClass({
                label: label,
                onClick: function(){
                    // create the dialog if it doesn't already exists
                    if (dialog_id != null){
                        var dialog = dijit.byId(dialog_id);
                        if (dialog == null){
                            // get the data_id
                            if (data_id != null){
                                if (typeof(data_id) == 'function') {
                                    dialog = content_creator(data_id());
                                } else {
                                    dialog = content_creator(data_id);
                                }
                            }
                        }
                        
                        // set the field updater
                        dialog.set(
                            'related_field_updater',
                            related_field_updater
                        );
                        
                        // show the dialog
                        dialog.show();
                    }
                }
            }, attach_to);
            
//            if (attach_to){
//                domConstruct.attach(widget, attach_to);
//                widget.attach(attach_to);
//            }
            
            return widget;
        };
        
        // ********************************************************************
        // PROJECT
        create_add_project_dialog = function (){
            return new DialogSimple({
                id: 'add_project_dialog',
                title: 'Add Project',
                href: '/add/project',
                resize: true,
                style: 'width: auto; height auto; padding: 0px;',
                executeScripts: true
            });
        };
        
        create_edit_project_dialog = function(project_id){
            return new DialogSimple({
                id: 'edit_project_dialog',
                title: 'Edit Project',
                href: '/edit/project/' + project_id,
                resize: true,
                style: 'width: auto; height: auto; padding 0px;',
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
                style: 'width: auto; height auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_image_format_dialog = function(image_format_id){
            return new DialogSimple({
                id: 'edit_image_format_dialog',
                title: 'Edit Image Format',
                href: '/edit/image_format/' + image_format_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            }); 
        };
        
        create_edit_structure_dialog = function(structure_id){
            return new DialogSimple({
                id: 'edit_structure_dialog',
                title: 'Edit Structure',
                href: '/edit/structure/' + structure_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_user_dialog = function(user_id){
            var myDialog = new DialogSimple({
                id: 'edit_user_dialog',
                title: 'Edit User',
                href: 'edit/user/' + user_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_filename_template_dialog = function(filename_template_id){
            var myDialog = new DialogSimple({
                id: 'edit_filename_template_dialog',
                title: 'Edit Filename Template',
                href: 'edit/filename_template/' + filename_template_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_repository_dialog = function(repo_id){
            return new DialogSimple({
                id: 'edit_repository_dialog',
                title: 'Edit Repository',
                href: '/edit/repository/' + repo_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_status_list_dialog = function(status_list_id){
            return new DialogSimple({
                id: 'edit_status_list_dialog',
                title: 'Edit Status List',
                href: '/edit/status_list/' + status_list_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_status_dialog = function(status_id){
            return new DialogSimple({
                id: 'edit_status_dialog',
                title: 'Edit Status',
                href: '/edit/status/' + status_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_shot_dialog = function(shot_id){
            return new DialogSimple({
                id: 'edit_shot_dialog',
                title: 'Edit Shot',
                href: '/edit/shot/' + shot_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_sequence_dialog = function(sequence_id){
            return new DialogSimple({
                id: 'edit_sequence_dialog',
                title: 'Edit Sequence',
                href: '/edit/sequence/' + sequence_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
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
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
        
        create_edit_task_dialog = function(task_id){
            return new DialogSimple({
                id: 'edit_task_dialog',
                title: 'Edit Task',
                href: '/edit/task/' + task_id,
                resize: true,
                style: 'width: auto; height: auto; padding: 0px',
                executeScripts: true
            });
        };
   });

