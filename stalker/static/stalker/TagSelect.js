// stalker.TagSelect
define([
    'require',
    'dojo/_base/declare', 'dijit/_WidgetBase', 'dijit/_TemplatedMixin',
    'dojo/text!stalker/templates/TagSelect.html',
    'dojo/_base/lang', 'dojo/dom-construct', 'dijit/form/Button',
    'dijit/form/FilteringSelect', 'dojo/on', 'dojo/domReady!'
], function(require, declare, _WidgetBase, _TemplatedMixin, template, lang,
            domConstruct, Button, FilteringSelect, on){
    return declare('stalker.TagSelect', [_WidgetBase, _TemplatedMixin],
        {
            templateString: template,
            
            name: null,
            store: null,
            
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
            
            baseClass: 'tagSelect',
            
            constructor: function stalker_tagSelect_constructor(args){
                if (args){
                    lang.mixin(this, args);
                }
            },
            
            startup: function stalker_tagSelect_startup(){
                this.inherited(arguments);
                this.filtering_select.startup();
            },
            
            postCreate: function tagSelect_postCreate(){
                // Run any parent postCreate processes - can be done at any point
                this.inherited(arguments);
                
                // Get a DOM node reference for the root of our widget
                var parent = this;
                var domNode = this.domNode;
                
                var input_widget_ap = this.input_widget_ap;
                var button_list_ap = this.tag_list_ap;
                
                this.tags = [];
                
                // create the filtering select with the given arguments
                this.filtering_select = new FilteringSelect({},
                    domConstruct.create("div", {}, input_widget_ap)
                );
                
                // connect th onChange method
                on(
                    this.filtering_select,
                    'change',
                    lang.hitch(this, function(){
                        var item = this.filtering_select.item;
                        if (item != null){
                            var current_label = item.name;
                            if (current_label != ''){
                                var current_id = this.filtering_select.value;
                                
                                // add a new button to the the tagList
                                var button = new Button({
                                    label: current_label,
                                    value: current_id,
                                    iconClass: 'dijitEditorIcon dijitEditorIconDelete'
                                }, domConstruct.create('div', null, button_list_ap));
                                button.startup();
                                
                                // style the button
                                var dNode = button.domNode;
                                dNode.children[0].style.borderRadius = '25px';
                                dNode.children[0].style.height = '13px';
                                
                                // replace the icon to the end
                                domConstruct.place(
                                    button.iconNode,
                                    button.containerNode,
                                    'after'
                                );
                                
                                // button resize and replace icon picture
                                button.iconNode.style.backgroundSize = '414px';
                                button.iconNode.style.backgroundPosition = '-54px';
                                button.iconNode.style.width = '9px';
                                button.iconNode.style.height = '9px';
                                
                                
                                // 414 px size
                                // -54 px offset
                                // 9px 9px icon size
                                
                                
                                on(button, 'click',
                                    lang.hitch(this, function(){
                                        // add the value back to the store
                                        var id = button.value;
                                        var name = button.label;
                                        this.store.add({
                                            id: id,
                                            name: name
                                        });
                                        // remove it self from the tags list
                                        var index = this.tags.indexOf(button);
                                        this.tags.pop(index);
                                        
                                        // destroy it self
                                        button.destroyRecursive();
                                    })
                                );
                                
                                
                                // add the button as a tag to this widget
                                this.tags.push(button);
                                
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




