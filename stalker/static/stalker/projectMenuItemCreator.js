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
], function (JsonRest, MenuItem, MenuSeparator, DropDownMenu, PopupMenuItem,
             PopupMenuBarItem, dialogs, dialogCaller) {

    var projectMenuItemCreator = function (kwargs) {

        var label = kwargs.label;
        var dataId = kwargs.dataId;




        var create_project_setting_DropDownMenu = function (pID) {

            var project_setting_DropDownMenu = new DropDownMenu({

            });

            // --------
            // View Project
            project_setting_DropDownMenu.addChild(
                    new MenuItem({
                        label: 'View',
                        dataId: pID,
                        onClick: function () {
                            central_content_pane.set(
                                    'href',
                                    'view/project/' + this.get('dataId')
                            );
                            central_content_pane.refresh();
                        }
                    })
            );

            // --------
            {% if has_permission('Update_Project') %}
                // Update Project
                project_setting_DropDownMenu.addChild(
                        dialogCaller({
                            label: 'Update',
                            dialog_id: 'project_dialog',
                            content_creator: dialogs.update_project_dialog,
                            widget_type: 'MenuItem',
                            data_id: pID

                        })
                );
            {% endif %}

            project_setting_DropDownMenu.addChild(
                    new MenuSeparator({})
            );

            // --------
            {% if has_permission('Create_Asset') %}
                // Asset
                project_setting_DropDownMenu.addChild(
                        dialogCaller({
                            label: 'New Asset',
                            dialog_id: 'asset_dialog',
                            content_creator: dialogs.create_asset_dialog,
                            widget_type: 'MenuItem',
                            data_id: pID

                        })
                );
            {% endif %}

            // --------
            {% if has_permission('Create_Sequence') %}
                // Sequence
                project_setting_DropDownMenu.addChild(
                        dialogCaller({
                            label: 'New Sequence',
                            dialog_id: 'sequence_dialog',
                            content_creator: dialogs.create_sequence_dialog,
                            widget_type: 'MenuItem',
                            data_id: pID
                        })
                );
            {% endif %}

            // ----
            {% if has_permission('Create_Shot') %}
                // Shot
                project_setting_DropDownMenu.addChild(
                        dialogCaller({
                            label: 'New Shot',
                            dialog_id: 'shot_dialog',
                            content_creator: dialogs.create_shot_dialog,
                            widget_type: 'MenuItem',
                            data_id: pID
                        })
                );
            {% endif %}

            {% if has_permission('Update_User') %}
                project_setting_DropDownMenu.addChild(
                        new MenuSeparator({})
                );

                project_setting_DropDownMenu.addChild(
                        dialogCaller({
                            label: 'Append User',
                            dialog_id: 'append_user_dialog',
                            content_creator: dialogs.append_user_dialog,
                            widget_type: 'MenuItem',
                            data_id: pID
                        })
                );
            {% endif %}

            return project_setting_DropDownMenu;

        };
    }



    return projectMenuItemCreator;
});
