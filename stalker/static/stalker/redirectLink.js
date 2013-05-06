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

define(['dijit/registry', 'dojo/on', 'dojo/query'],
    function (registry, on, query) {
        // ********************************************************************
        // GO TO LINK
        //
        //
        var redirectLink = function (kwargs) {
            var target = kwargs.target;
            var address = kwargs.address;

            var contentPane = registry.byId(target);
            if (contentPane) {
                contentPane.set('href', address);
                contentPane.refresh();
            }


        };
        return redirectLink;
    });
