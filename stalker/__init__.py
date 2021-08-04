# -*- coding: utf-8 -*-
"""Stalker is a Production Asset Management System (ProdAM) designed for
Animation and VFX Studios.

See docs for more information.
"""

import sys

__version__ = '0.2.26'

__title__ = "stalker"
__description__ = 'A Production Asset Management (ProdAM) System'
__uri__ = 'http://github.com/eoyilmaz/stalker'
__doc__ = "%s <%s>" % (__description__, __uri__)

__author__ = "Erkan Ozgur Yilmaz"
__email__ = 'eoyilmaz@gmail.com'

__license__ = 'LGPLv3'
__copyright__ = "Copyright (C) 2009-2018 Erkan Ozgur Yilmaz"


__string_types__ = []
if sys.version_info[0] >= 3:  # Python 3
    __string_types__ = tuple([str])
else:  # Python 2
    __string_types__ = tuple([str, unicode])


# before anything about stalker create the defaults
# use this instance
from stalker import config
defaults = config.Config()

from stalker.models.auth import Group, Permission, User, LocalSession, Role, AuthenticationLog
from stalker.models.asset import Asset
from stalker.models.budget import Budget, BudgetEntry, Good, PriceList, Invoice, Payment
from stalker.models.client import Client, ClientUser
from stalker.models.department import Department, DepartmentUser
from stalker.models.entity import SimpleEntity, Entity, EntityGroup
from stalker.models.format import ImageFormat
from stalker.models.link import Link
from stalker.models.message import Message
from stalker.models.mixins import (ACLMixin, AmountMixin, CodeMixin, DAGMixin,
                                   DateRangeMixin, ProjectMixin,
                                   ReferenceMixin, ScheduleMixin, StatusMixin,
                                   TargetEntityTypeMixin, UnitMixin,
                                   WorkingHoursMixin)
from stalker.models.note import Note
from stalker.models.project import Project, ProjectUser, ProjectClient, ProjectRepository
from stalker.models.review import Review, Daily, DailyLink
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

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
