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

define(['dijit/registry', 'dojo/on', 'dojo/query'],
    function(registry, on, query){
        // ********************************************************************
        // GO TO LINK
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
        var gotoLink = function(kwargs){
            var target = kwargs.target || null;
            
            if (target){
                var contentPane = registry.byId(target);
                
                if (contentPane){
                    // get the Link Elements
                    var dataLinks = query('.DataLink');
                    
                    for (var i=0; i<dataLinks.length; i++){
                        on(dataLinks[i], 'click', function(){
                            contentPane.set('href', this.getAttribute('stalker_href'));
                            contentPane.reset();
                        });
                    }
                }
            }
        };
        return gotoLink;
});
