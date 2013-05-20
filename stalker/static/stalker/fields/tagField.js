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
    'stalker/TagSelect',
    'stalker/fieldUpdater'
], function (JsonRest, TagSelect, fieldUpdater) {

    // ********************************************************************
    // tagField
    // 
    // An input field for tags.
    // 
    // PARAMETERS
    // 
    // attach_to:
    //   a dom element to attach the created tagSelect field
    // 
    // selected_tags:
    //   a list of integers showing the selected tags
    return function (kwargs) {

        var attach_to = kwargs['attach_to'] || null;
        var selected_tags = kwargs['selected_tags'] || [];

        // ********************************************************************
        // Tags
        var tags_jsonRest = new JsonRest({
            target: 'get/tags'
        });

        var tags_tagSelect = new TagSelect({
            name: 'tag_names',
            type: 'ComboBox'
        }, attach_to);

        // The Updater
        var tags_field_updater = fieldUpdater({
            memory: tags_jsonRest,
            widget: tags_tagSelect,
            selected: selected_tags
        });
        tags_field_updater({animate: false});

        return tags_tagSelect;
    };
});
