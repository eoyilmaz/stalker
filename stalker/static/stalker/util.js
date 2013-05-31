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

define(['exports',  'dojo/domReady!'],
    function (exports) {
        // module:
        //      stalker/dialogs
        // summary:
        //      This module defines the core dojo DOM construction API.

        // TODOC: summary not showing up in output, see https://github.com/csnover/js-doc-parse/issues/42

        // ********************************************************************
        exports.extract_from_time = function extract_form_time(kwargs) {
            var date = kwargs['date'] || new Date();
            return 'T' + ("00" + date.getHours()).slice(-2) + ':' + ("00" + date.getMinutes()).slice(-2) + ':00';
        };
    });