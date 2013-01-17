require(['dijit/registry', 'dojo/_base/lang','dojo/request/xhr',
    'dojo/store/Memory', 'dojox/widget/DialogSimple', 'dijit/form/Button',
    'dojo/_base/fx', 'dojo/dom-style'],
    function(registry, lang, xhr, Memory, DialogSimple, Button, fx, style){
        
        // ********************************************************************
        // DO_SUBMIT
        // 
        // A helper function for form submission.
        // 
        // Helps to submit the data and update a related field together. Uses
        // Deferred post and waits for the data to be send before updating the
        // related field if any.
        // 
        // 
        // PARAMETERS
        // 
        // dialog:
        //   the dialog to reset and destroy
        // 
        // form:
        //   the form to get the data form
        // 
        // additional_data:
        //   additional data to append to the form data
        // 
        // url:
        //   the url to submit the data to
        // 
        // method:
        //   the method POST or GET
        // 
        submit_form = function(kwargs){
            var dialog = kwargs.dialog;
            var form = kwargs.form;
            var additional_data = kwargs.additional_data || {};
            var url = kwargs.url;
            var method = kwargs.method;
            
            if (form.validate()){
                // get the form data
                var form_data = form.get('value');
                form_data = lang.mixin(form_data, additional_data);
                
                var deferred = xhr.post(
                  url,
                  {
                    method: method,
                    data: form_data
                  }
                );
                
                deferred.then(function(){
                  // update the caller dialog
                  var related_field_updater = dialog.get(
                      'related_field_updater'
                  );
                  if (related_field_updater != null){
                    related_field_updater();
                  }
                  // destroy the dialog
                  dialog.reset();
                  dialog.destroyRecursive();
                });
            }
        };
        
        // ********************************************************************
        // FIELD_UPDATER
        // 
        // Returns a function which when called updates a field
        //
        // memory:
        //  the JsonRest instance
        // 
        // widget:
        //  the widget to update the data to
        // 
        // selected:
        //  stores what is selected among the data
        // 
        field_updater = function(kwargs){
            var memory = kwargs.memory;
            var widget = kwargs.widget;
            var selected = kwargs.selected || [];
            
            return function(){
                var animate = arguments[0] || true;
                var result = memory.query().then(function(data){
                    widget.reset();
                    
                    // if the widget is a MultiSelect
                    if (widget.declaredClass == "dijit.form.MultiSelect"){
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
                    } else {
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
        // CREATE ADD EDIT DATA BUTTON
        //
        // Creates a button to add/edit some data depending on to the given
        // dialog.
        // 
        // PARAMETERS
        // 
        // button_label:
        //   The label of the add button, default is 'Add'
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
        // data_id_getter:
        //   if we already have some id for the data, let say if we are
        //   adding a new Sequence to a Project then this is the function
        //   that returns the Project.id or if we are editing a data then
        //   this is the function returning the edited data id.
        //   
        //   It is a function because it needs to have the current value of
        //   the edited data, so it can not be a direct value.
        //
        // related_field_updater:
        //   a function object without any parameters which will update the
        //   the related field which this form is adding data to.
        create_add_edit_data_button = function(kwargs){
            var button_label = kwargs.button_label || 'Add';
            var dialog_id = kwargs.dialog_id;
            var content_creator = kwargs.content_creator;
            var attach_to = kwargs.attach_to;
            var data_id_getter = kwargs.data_id_getter|| function(){};
            var related_field_updater = kwargs.related_field_updater;
            
            return new Button({
                label: button_label,
                type: 'Button',
                onClick: function(){
                    // create the dialog if it doesn't already exists
                    var dialog = dijit.byId(dialog_id);
                    if (dialog == null){
                        dialog = content_creator(data_id_getter());
                    }
                    
                    // set the field updater
                    dialog.set('related_field_updater', related_field_updater);
                    
                    // show the dialog
                    dialog.show();
                }
            }, attach_to);
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
        create_add_status_list_dialog = function(){
            return new DialogSimple({
                id: 'add_status_list_dialog',
                title: 'Add Status List',
                href: '/add/status_list',
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

