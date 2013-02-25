define(['dijit/form/Button', 'dijit/MenuItem'],
    function(Button, MenuItem){
        // ********************************************************************
        // DialogCaller
        //
        // Creates a widget (a button or a menuItem) which calls the given
        // dialog and also works together with stalker.submitForm and updates
        // the given field with the newly created or edited value.
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
        
        // it calls a dialog which generally adds or edits a data
        // but it is not limited with that, it just calls the dialog
        
        var dialogCaller = function(kwargs){
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
            
            return widget;
        };
        
        return dialogCaller;
    }
);

