define(['dojo/request/xhr', 'dojo/_base/lang'],
    function(xhr, lang){
    // ********************************************************************
    // SUBMIT FORM
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
    // dialog: dijit.dialog.Dialog
    //   the dialog to reset and destroy
    // 
    // form: dijit.form.Form
    //   the form to get the data form
    // 
    // additional_data: Dictionary
    //   additional data to append to the form data
    // 
    // url: String
    //   the url to submit the data to
    // 
    // method: String
    //   the method POST or GET
    // 
    var submitForm = function(kwargs){
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
            }, function(err){
                // Do something when the process errors out
                alert(err);
            });
            
        }
    };
    return submitForm;
});
