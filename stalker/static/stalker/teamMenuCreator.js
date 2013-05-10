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
    'dojo/store/JsonRest',
    
    'dijit/MenuItem',
    'dijit/MenuSeparator',
    'dijit/DropDownMenu',
    'dijit/PopupMenuItem',
    'dijit/PopupMenuBarItem',
    
    'stalker/dialogs',
    'stalker/dialogCaller'
    ], function(JsonRest, MenuItem, MenuSeparator, DropDownMenu,
                PopupMenuItem, PopupMenuBarItem, dialogs, dialogCaller){
    
    var teamMenuCreator = function(kwargs){
        
        var team_is_singular = kwargs.team_is_singular || false;
        var menu_to_attach = kwargs.menu_to_attach;
        var entity_type_name = kwargs.entity_type_name;
        var view_entity_url = kwargs.view_entity_url;
        var query_entity_url = kwargs.query_entity_url;
        var content_pane_to_update = kwargs.content_pane_to_update;
        
        var new_team_dialog_id = kwargs.new_team_dialog_id;
        var new_team_dialog_content_creator = kwargs.new_team_dialog_content_creator;
        
        var entity_type_name_title = entity_type_name.slice(0, 1).toUpperCase() + 
                                     entity_type_name.slice(1).toLowerCase();
        var entity_type_name_plural = kwargs.entity_type_name_plural || entity_type_name_title + 's';
        
        // Main Menu PopUpMenu
        
        var team_main_menu = new DropDownMenu();

        
        var team_main_popup_menu = new PopupMenuItem({
            label: entity_type_name_plural,
            popup: team_main_menu
        });
        
        // attach it to the main menu
        menu_to_attach.addChild(team_main_popup_menu);
        
        // Team Menu
        // Creates the main team menu content
        var create_team_DropDownMenu = function (team) {
            
            var tName = team.name;
            var tID = team.id;
            
            if (!team_is_singular){
                // Create a normal DropDownMenu (ex: for Departments and Groups)

                var team_DropDownMenu = new DropDownMenu();
                // --------
                // View Team
                team_DropDownMenu.addChild(
                    new MenuItem({
                        label: 'View',
                        dataId: tID,
                        onClick: function () {
                            content_pane_to_update.set(
                                'href',
                                view_entity_url + this.get('dataId')
                            );
                            content_pane_to_update.refresh();
                        }
                    })
                );

            
                
                // ----------
                // New User
                team_DropDownMenu.addChild(
                    dialogCaller({
                        label: 'New User',
                        dialog_id: 'create_user_dialog',
                        content_creator: dialogs.create_user_dialog,
                        widget_type: 'MenuItem',
                        data_id: tID
                    })
                );
                
                team_DropDownMenu.addChild(
                    new MenuSeparator({})
                );
                
                // List Users
                var users_memory = new JsonRest({
                    target: 'get/users_byEntity/' + tID
                });
                
                var result = users_memory.query().then(function (data) {
                    for (var i = 0; i < data.length; i++) {
                        var user_id = data[i]['id'];
                        var user_name = data[i]['name'];
                        team_DropDownMenu.addChild(
                            new MenuItem({
                                label: user_name,
                                dataId: user_id,
                                onClick: function () {
                                    content_pane_to_update.set(
                                            'href',
                                            'view/user/' + this.get('dataId')
                                    );
                                    content_pane_to_update.refresh();
                                }
                            })
                        );
                    }
                });
                
                
                var team_PopupMenuItem = new PopupMenuItem({
                    label: tName,
                    dataId: tID,
                    popup: team_DropDownMenu
                });
                
                return team_PopupMenuItem;
                
            } else {
                // Just return a MenuItem (ex: for Users)
                var team_MenuItem = new MenuItem({
                        label: tName,
                        dataId: tID,
                        onClick: function () {
                            content_pane_to_update.set(
                                'href',
                                view_entity_url + this.get('dataId')
                            );
                            content_pane_to_update.refresh();
                        }
                });
                
                return team_MenuItem;
            }
        };

        
        
        
        // Team Memory
        var team_memory = new JsonRest({
            target: query_entity_url
        });
        
        // Team Updater
        var team_DropDownMenu_updater = function () {
            // delete the current items
            var items = team_main_menu.getChildren();
            for (var i = 0; i < items.length; i++) {
                items[i].destroyRecursive();
            }
            
            // query new items
            var result = team_memory.query().then(function (data) {
                
                // ----------
                // New Team
                team_main_menu.addChild(
                    dialogCaller({
                        label: 'New ' + entity_type_name_title,
                        dialog_id: new_team_dialog_id,
                        content_creator: new_team_dialog_content_creator,
                        widget_type: 'MenuItem',
                        related_field_updater: team_DropDownMenu_updater
                    })
                );
                
                team_main_menu.addChild(
                    new MenuSeparator({})
                );
                
                // --------------------------------
                // Team Members
                for (var i = 0; i < data.length; i++) {
                    team_main_menu.addChild(
                        
                        create_team_DropDownMenu(data[i])
                        
                    );
                }


            });
        };
        
        
        // use the updater to create the menu itself
        team_DropDownMenu_updater();
    };
    
    return teamMenuCreator;
});
