// Stalker a Production Asset Management System
// Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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

define([
    'dijit/Menu',
    'dijit/MenuItem',
    
    'stalker/dialogs',
    'stalker/dialogCreator',
    
    'dojo/domReady!'
], function (Menu, MenuItem, dialogs, dialogCreator) {
    
    // ************************************************************************
    // Thumbnail Menu
    // 
    return function (kwargs){
        var targetNodeIds = kwargs['targetNodeIds'];
        var selector = kwargs['selector'];
        var leftClickToOpen = kwargs['leftClickToOpen'] || true;
        var entity_id = kwargs['entity_id'] || -1;
        var related_field_updater = kwargs['related_field_updater'] || function(){};
        
        
        // create the thumbnail upload menu
        var t_menu = new Menu({
            targetNodeIds: targetNodeIds,
            selector: selector,
            leftClickToOpen: leftClickToOpen
        });
        
        var t_menuItem_creator = function () {
            return new MenuItem({
                label: 'Upload Thumbnail...',
                onClick: function () {
                    var node = this.getParent().currentTarget;
                    var dialog = dialogCreator({
                        dialog_id: 'upload_thumbnail_dialog',
                        data_id: entity_id,
                        content_creator: dialogs.upload_thumbnail_dialog,
                        related_field_updater: related_field_updater
                    });
                    dialog.show();
                }
            });
        };

        t_menu.addChild(t_menuItem_creator());
    };
});
