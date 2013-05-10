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

define([
    'dojo/dom-construct',
    'dojo/query',
    'dojo/store/Memory',
    'dojo/_base/fx'
], function (domConstruct, dojoQuery, Memory, fx) {
    // ************************************************************************
    // FIELD_UPDATER
    // 
    // Returns a function which when called updates a field
    //
    // memory: dojo.store.JsonRest
    //  the JsonRest instance
    // 
    // widget: dojo._WidgetBase
    //  the widget to update the data to
    //
    // query_data: String or function
    //  the data to be queried to, Anonymous functions are accepted
    // 
    // selected: Array
    //  stores what is selected among the data
    // 
    var fieldUpdater = function (kwargs) {
        var memory = kwargs.memory;
        var widget = kwargs.widget;
        var callBackFunction = kwargs.callBack || function (arg) {
        };
        var query_data = kwargs.query_data || null;
        var selected = kwargs.selected || [];
        var placeHolder = kwargs.placeHolder || '';

        // set default placeHolder


        return function () {
            var animate = arguments[0] || true;
            var query;

            if (query_data != null) {
                var data_id;
                if (typeof(query_data) == 'function') {
                    data_id = query_data();
                } else {
                    data_id = query_data;
                }

                if (data_id == '') {
                    return;
                }

                query = memory.query(data_id);
            } else {
                query = memory.query();
            }

            return query.then(function (data) {

                // if the widget is a MultiSelect
                if (widget.declaredClass == "dijit.form.MultiSelect") {
                    widget.reset();
                    // add options manually
                    // remove the previous options first
                    dojoQuery('option', widget.domNode).forEach(
                        function (opt, idx, arr) {
                            domConstruct.destroy(opt);
                        }
                    );

                    // add options
                    for (var i = 0; i < data.length; i++) {
                        domConstruct.create(
                            'option',
                            {
                                'value': data[i].id,
                                'innerHTML': data[i].name
                            },
                            widget.domNode
                        );
                    }

                    // select selected
                    if (selected.length) {
                        widget.set('value', selected);
                    }
                } else if (widget.declaredClass == 'dojox.grid.DataGrid') {
                    // just call render
                    widget.render();
                } else {
                    // store current value
                    var old_value = widget.get('value');
                    try {
                        widget.reset();
                    } catch (err) {
                        // don't do anything
                    }
                    // set the data normally
                    widget.set('store', new Memory({data: data}));

                    //console.log('data.length: '+ widget.label + ' : ' + data.length);

                    if (data.length > 0) {
                        if (widget.label) {
                            placeHolder = 'Select a ' + widget.label;
                        }
                        else {
                            placeHolder = 'Select an item from list';
                        }
                        widget.set('placeHolder', placeHolder);
//
                        if (widget.declaredClass != 'dijit.form.FilteringSelect') {
                            try {
                                widget.attr('value', data[0].id);
                            } catch (err) {
                                // don't do anything
                            }
                        }

                        // restore the old value
                        try {
                            if (old_value) {
                                widget.set('value', old_value);
                            }
                        } catch (err) {
                            // don't do anything
                        }

                    } else {
                        if (widget.label) {
                            placeHolder = 'Create New ' + widget.label;
                        } else {
                            placeHolder = 'Create New';
                        }
                        widget.set('placeHolder', placeHolder);
                    }
                    if (selected.length) {
                        widget.set('value', selected);
                    }
                }

                if (animate == true) {
                    // animate the field to indicate it is updated;

                    var domNode = widget.domNode;
                    var bgColor = domNode.style.backgroundColor;
                    fx.animateProperty({
                        node: domNode,
                        duration: 500,
                        properties: {
                            backgroundColor: {
                                start: "#00ff00",
                                end: bgColor
                            }
                        }
                    }).play();
                }

                // TODO: callBackFunction should get more then the data
                //   use kwargs
                //   kwargs.data
                //   kwargs.widget
                callBackFunction(data);
            });
        };
    };
    return fieldUpdater;
});
