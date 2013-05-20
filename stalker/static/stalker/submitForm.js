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

define(['dojo/request/xhr', 'dojo/_base/lang'],
    function (xhr, lang) {
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
        var submitForm = function (kwargs) {
            var dialog = kwargs.dialog;
            var form = kwargs.form;
            var additional_data = kwargs.additional_data || {};
            var url = kwargs.url;
            var method = kwargs.method;

            if (form.validate()) {
                // enable all disable fields
                var form_children = form.getChildren();
                var disabled_children = [];
                var child_is_disabled;
                for (var i=0 ; i < form_children.length; i++){
                    child_is_disabled = form_children[i].get('disabled');
                    if (child_is_disabled){
                        form_children[i].set('disabled', false);
                        disabled_children.push(form_children[i]);
                    }
                }
                
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
                
                deferred.then(function () {
                    // update the caller dialog
                    var related_field_updater = dialog.get(
                        'related_field_updater'
                    );
                    if (related_field_updater != null) {
                        related_field_updater();
                    }
                    // destroy the dialog
                    dialog.reset();
                    dialog.destroyRecursive();
                }, function (err) {
                    // Do something when the process errors out
                    console.error(err);
                    alert(err);
                    // re-disable enabled children
                    for (var i=0 ; i < disabled_children.length ; i++){
                        disabled_children[i].set('disabled', true);
                    }
                });

            }
        };
        return submitForm;
    });
