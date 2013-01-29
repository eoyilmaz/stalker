// stalker.TagSelect
// 
// A customized widget for Tag creation
//
// TODO: It should either create a FilteringSelect or a TextField by the choice of User
// 
define([
    'require',
    'dojo/_base/declare', 'dijit/_WidgetBase', 'dijit/_TemplatedMixin',
    'dojo/text!stalker/templates/TagSelect.html',
    'dojo/_base/lang', 'dojo/dom-construct', 'stalker/Tag',
    'dijit/form/FilteringSelect', 'dojo/on', 'dojo/domReady!'
], function(require, declare, _WidgetBase, _TemplatedMixin, template, lang,
            domConstruct, Tag, FilteringSelect, on){
    return declare('stalker.TagSelect', [_WidgetBase, _TemplatedMixin],
        {
            templateString: template,
            
            name: null,
            store: null,
            
            required: false,
            
            tags: [],
            filtering_select: null,
            
            button_div: null,
            
            _setNameAttr: function(value){
                if (this.filtering_select){
                    this.filtering_select.set('name', value);
                }
            },
            
            _setStoreAttr: function(value){
                if (this.filtering_select){
                    this.filtering_select.set('store', value);
                    this.store = value;
                }
            },
            
            _getValueAttr: function(){
                // return the value of the buttons
                var value = [];
                for(var i; i < this.tags.length; i++){
                    value.push(this.tags.get('value'));
                }
                return value;
            },
            
            _setDisabledAttr: function(value){
                // set the filtering select and all the tags disabled
                this.filtering_select.set('disabled', value);
                for (var i=0; i < this.tags.length; i++){
                    this.tags[i].set('disabled', value);
                }
            },
            
            isValid: function(){
                console.log('TagSelect is validating!!!!');
            },
            
            baseClass: 'stalker.tagSelect',
            
            constructor: function stalker_tagSelect_constructor(args){
                if (args){
                    lang.mixin(this, args);
                }
            },
            
            startup: function stalker_tagSelect_startup(){
                this.inherited(arguments);
                this.filtering_select.startup();
            },
            
            // 
            // adds the given value to the store again
            // 
            // TODO: if this is a FilteringSelect use {id, name} but if it is a TextField
            //       do nothing
            add_value: function(value){
                // add the value back to the store
                this.store.add(value);
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
                var value = tag.getValue();
                this.store.add(value);
                
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
                
                // create the filtering select with the given arguments
                this.filtering_select = new FilteringSelect({
                        required: false
                    },
                    domConstruct.create("div", {}, input_widget_ap)
                );
                
                // connect the `change` event
                on(this.filtering_select, 'change',
                    lang.hitch(this, function(){ // to protect `this`
                        var item = this.filtering_select.item;
                        if (item != null){
                            var current_label = item.name;
                            if (current_label != ''){
                                var current_id = this.filtering_select.value;
                                
                                // add a new button to the the tagList
                                var tag = new Tag({
                                    label: current_label,
                                    value: current_id
                                }, domConstruct.create('div', null, tag_list_ap));
                                tag.startup();
                                
                                // attach self to the tag
                                tag.tagSelect = this;
                                
                                // add the button as a tag to this widget
                                this.tags.push(tag);
                                
                                // delete the current value from the FilteringSelect
                                this.filtering_select.set('value', '');
                                
                                // also remove the current value from the store
                                this.store.remove(current_id);
                            }
                        }
                    })
                );
            }
    });
});




