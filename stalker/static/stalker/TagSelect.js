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
            
            name: null,
            store: null,
            
            required: false,
            
            tags: [],
            input_field_widget: null,
            type: 'FilteringSelect',
            
            selected: [], // pre defined selection list
            
            button_div: null,
            
            _setNameAttr: function(value){
                console.log('TagSelect._setNameAttr is running!!!');
                if (this.input_field_widget){
                    this.input_field_widget.set('name', value);
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
                console.log('TagSelect._getValueAttr is running!!!');
                // return the value of the buttons
                var value = [];
                for(var i=0; i < this.tags.length; i++){
                    value.push(this.tags[i].value);
                }
                return value;
            },
            
            _setDisabledAttr: function(value){
                // set the input field widget and all the tags disabled
                this.input_field_widget.set('disabled', value);
                for (var i=0; i < this.tags.length; i++){
                    this.tags[i].set('disabled', value);
                }
            },
            
            isValid: function(){
                console.log('TagSelect.isValid is running!');
            },
            
            validator: function(){
                console.log('TagSelect.validator is running!');
            },
            
            baseClass: 'stalker.tagSelect',
            
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
                this.input_field_widget.reset();
                for (var i=0; i < this.tags.length; i++){
                    this.tags[i].destroyRecursive();
                }
            },
            
            
            // connect the `change` event
            create_tag: lang.hitch(this, function(){ // to protect `this`
                
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
                        this.input_field_widget.set('value', '');
                        
                        // also remove the current value from the store
                        if (this.store){
                            this.store.remove(current_id);
                        } 
                        
                    }
                }
            }),
            
            
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
                
                on(this.input_field_widget, 'change', this.create_tag);
                
                // create the tags for the selected list
                for (var i=0; i < this.selected.length; i++){
                    // create the items
                }
            }
    });
});




