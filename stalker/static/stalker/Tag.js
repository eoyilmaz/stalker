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
// stalker.Tag
// 
// A tag like widget with a close icon
//
define([
    'dojo/_base/declare', 'dojo/dom-construct', 'dijit/form/Button'
], function(declare, domConstruct, Button){
        return declare('stalker.Tag', Button, {
            
            tagSelect: null,
            label: '',
            value: '',
            
            _getValueAttr: function(){
                return {
                    id: this.value,
                    name: this.label
                };
            },
            
            //_setValueAttr: function(value){
            //    // value is a id, name pair
            //    this.set('value', value.id);
            //    this.set('label', value.name);
            //},
            
            postCreate: function tag_postCreate(){
                this.inherited(arguments);
                this.style_tag();
            },
            
            // replace onClick
            _onClick: function(/*Event*/e){
                // it still runs even it is disabled
                // so prevent it
                if (this.disabled){
                    return;
                }
                
                // if there is a tagSelect, remove it self
                // if not just kill itself
                if (this.tagSelect){
                    this.tagSelect.remove_tag(this);
                }
                
                // and destroy itself
                this.destroyRecursive();
                
                // call user defined onClick
                return this.onClick(e);
            },
            
            // Set the tag style
            style_tag: function tag_style_tag(){
                var dNode = this.domNode;
                dNode.children[0].style.borderRadius = '25px';
                dNode.children[0].style.height = '16px';
                
                // replace the icon to the end
                domConstruct.place(
                    this.iconNode,
                    this.containerNode,
                    'after'
                );
                
                // set the icon
                this.set('iconClass',
                         'dijitEditorIcon dijitEditorIconDelete');
                
                // resize and replace icon picture
                this.iconNode.style.backgroundSize = '414px';
                this.iconNode.style.backgroundPosition = '-54px';
                this.iconNode.style.width = '9px';
                this.iconNode.style.height = '9px';
            }
        }
    )
});
