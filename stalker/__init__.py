# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
"""Stalker is a Production Asset Management System (ProdAM) designed for
Animation and VFX Studios.

See docs for more information.
"""

__version__ = '0.2.7.3'


# before anything about stalker create the defaults
from stalker.config import defaults

from stalker.models.auth import Group, Permission, User, LocalSession
from stalker.models.asset import Asset
from stalker.models.department import Department
from stalker.models.client import Client
from stalker.models.entity import SimpleEntity, Entity
from stalker.models.format import ImageFormat
from stalker.models.link import Link
from stalker.models.message import Message
from stalker.models.mixins import (ProjectMixin, ReferenceMixin,
                                   DateRangeMixin, StatusMixin,
                                   TargetEntityTypeMixin, CodeMixin,
                                   WorkingHoursMixin, ScheduleMixin)
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.review import Review
from stalker.models.repository import Repository
from stalker.models.scene import Scene
from stalker.models.schedulers import SchedulerBase, TaskJugglerScheduler
from stalker.models.sequence import Sequence
from stalker.models.shot import Shot
from stalker.models.status import Status, StatusList
from stalker.models.structure import Structure
from stalker.models.studio import Studio, WorkingHours, Vacation
from stalker.models.tag import Tag
from stalker.models.task import TimeLog, Task, TaskDependency
from stalker.models.template import FilenameTemplate
from stalker.models.ticket import Ticket, TicketLog
from stalker.models.type import Type, EntityType
from stalker.models.version import Version
from stalker.models.wiki import Page
from stalker.models.auth import group_finder

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
