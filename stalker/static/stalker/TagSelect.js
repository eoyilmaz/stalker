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
//
//
// stalker.TagSelect
// 
// A customized widget for Tag creation
//
// TODO: It should either create a FilteringSelect or a TextBox by the choice of User
// 
define([
    'require',
    'dojo/_base/declare', 'dijit/_WidgetBase', 'dijit/_TemplatedMixin',
    'dojo/text!stalker/templates/TagSelect.html',
    'dojo/_base/lang', 'dojo/dom-construct', 'dojo/dom-geometry', 'stalker/Tag',
    'dijit/form/FilteringSelect', 'dijit/form/TextBox', 'dojo/on', 'dojo/domReady!'
], function(require, declare, _WidgetBase, _TemplatedMixin, template, lang,
            domConstruct, domGeometry, Tag, FilteringSelect, TextBox, on){
    return declare('stalker.TagSelect', [_WidgetBase, _TemplatedMixin],
        {
            templateString: template,

            baseClass: 'stalker.tagSelect',

            name: null,
            store: null,

            required: false,

            tags: [],
            input_field_widget: null,
            type: 'FilteringSelect',

            selected: [], // pre defined selection list

            button_div: null,

            _setNameAttr: function(value){
                if (this.input_field_widget){
                    this.input_field_widget.set('name', value);
                }
            },

            _setStyleAttr: function(value){
                console.log(
                    'setting the TagSelect.input_field_widget.style: ', value
                );
                if (this.input_field_widget){
                    console.log('there is an input_field_widget');
                    this.input_field_widget.set('style', value);
                }
            },

            _setStoreAttr: function(value){
                if (this.input_field_widget){
                    this.input_field_widget.set('store', value);
                    this.store = value;
                }
            },

            // value: Array
            //      The value of this widget
            value: [],

            _getValueAttr: function(){
                // return the value of the buttons
                var value = [];
                for(var i=0; i < this.tags.length; i++){
                    value.push(this.tags[i].value);
                }
                return value;
            },

            _setValueAttr: function(value){
                // create the tags for the `selected` list
                var tag_value;
                var tag_label;
                var result;

                // remove all previous tags
                this.reset();

                for (var i=0; i < value.length; i++){
                    if (this.store){
                        // get the labels of the selected ids
                        result = this.store.query({id: value[i]});
                        if (result.length){
                            tag_label = result[0].name;
                        }
                    } else {
                        tag_label = value[i];
                    }
                    tag_value = value[i];

                    // create the items
                    if (tag_label != ''){
                        this.add_tag({
                            label: tag_label,
                            value: tag_value
                        });
                    }
                }
            },

            _setDisabledAttr: function(value){
                // set the input field widget and all the tags disabled
                this.input_field_widget.set('disabled', value);
                for (var i=0; i < this.tags.length; i++){
                    this.tags[i].set('disabled', value);
                }
            },

            isValid: function(){
                console.log('TagSelect.isValid is running!!!');
                if (this.required){
                    // check if there are any tags selected
                    return this.tags.length > 0;
                }
                return true;
            },

//            validate: function(){
//                this.inherited(arguments);
//                return this.isValid;
//            },
//            validator: function(){
//            },

            constructor: function stalker_tagSelect_constructor(args){
                if (args){
                    lang.mixin(this, args);
                }
            },

            startup: function stalker_tagSelect_startup(){
                this.inherited(arguments);
                this.input_field_widget.startup();
            },

            reset: function stalker_tagSelect_reset(){
                this.inherited(arguments);
                if (this.input_field_widget != null){
                    this.input_field_widget.reset();
                }
                for (var i=0; i < this.tags.length; i++){
                    this.tags[i].destroyRecursive();
                }
                this.tags = [];
            },


            // 
            // adds the given value to the store again
            // 
            // TODO: if this is a FilteringSelect use {id, name} but if it is a TextField
            //       do nothing
            add_value: function(value){
                // add the value back to the store
                if (this.store){
                    this.store.add(value);
                }
            },

            //
            // creates a Tag with the given label and value and removes the
            // given value from the store if there is a store and the given
            // value exists in the store
            // 
            // 
            // 
            add_tag: function(kwargs){
                var label = kwargs.label;
                var value = kwargs.value;

                if (label != null){
                    if (label != ''){
                        // add a new button to the the tagList
                        var tag = new Tag({
                            label: label,
                            value: value
                        }, domConstruct.create('div', null, this.tag_list_ap));
                        tag.startup();

                        // attach self to the tag
                        tag.tagSelect = this;

                        // add the button as a tag to this widget
                        this.tags.push(tag);

                        // delete the current value from the FilteringSelect
                        this.input_field_widget.set('value', '');

                        // also remove the current value from the store
                        if (this.store){
                            this.store.remove(value);
                        }

                    }
                }
            },


            //
            // removes the given tag from the tagList and returns the value of
            // the tag to the store
            // 
            remove_tag: function(/*stalker.Tag*/ tag){
                // check if it is really a Tag instance
                if (tag.declaredClass != 'stalker.Tag'){
                    // TODO: it can be an instance of a derived class
                    // don't bother doing anything with that
                    return;
                }

                // return the tag value to the store
                if (this.store){
                    var value = tag.getValue();
                    this.store.add(value);
                }

                // remove the tag from the tags list
                var index = this.tags.indexOf(tag);
                if (index != -1){
                    this.tags.splice(index, 1);
                }

                // destroy the tag
                tag.destroyRecursive();
            },

            postCreate: function tagSelect_postCreate(){
                // Run any parent postCreate processes - can be done at any point
                this.inherited(arguments);

                // Get a DOM node reference for the root of our widget
                var parent = this;
                var domNode = this.domNode;

                var input_widget_ap = this.input_widget_ap;
                var tag_list_ap = this.tag_list_ap;

                this.tags = [];

                // create the input field widget with the given arguments
                var WidgetClass = null;
                if (this.type == 'FilteringSelect'){
                    WidgetClass = FilteringSelect;
                } else if (this.type == 'TextBox') {
                    WidgetClass = TextBox;
                }

                this.input_field_widget = new WidgetClass({
                        required: false
                    }, domConstruct.create("div", {}, input_widget_ap)
                );

                // set the input_widget_ap width to limit the size of the
                // tag list
                var content_box = domGeometry.getContentBox(
                    this.input_field_widget.domNode
                );
                tag_list_ap.style.width = String(content_box.w) + 'px';

                var tag_create_func = lang.hitch(this, function(e){
                    var item;
                    var current_label;

                    if (this.type == 'FilteringSelect'){
                        item = this.input_field_widget.item;
                        if (item != null){
                            current_label = item.name;
                        }
                    } else if (this.type == 'TextBox'){
                        current_label = this.input_field_widget.value;
                    }

                    if (current_label != null){
                        if (current_label != ''){
                            var current_id = this.input_field_widget.value;

                            this.add_tag({
                                label: current_label,
                                value: current_id
                            });

                        }
                    }
                });

                // register the tag_create_func to `change` event
                on(this.input_field_widget, 'change', tag_create_func);

            }
        });
});




