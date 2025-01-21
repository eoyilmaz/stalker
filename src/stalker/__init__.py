# -*- coding: utf-8 -*-
"""Stalker is a Production Asset Management (ProdAM) designed for Animation/VFX Studios.

See docs for more information.
"""
from stalker.version import __version__  # noqa: F401
from stalker import config, log  # noqa: I100

if True:
    defaults: config.Config = config.Config()
from stalker.models.asset import Asset
from stalker.models.auth import (
    AuthenticationLog,
    Group,
    LocalSession,
    Permission,
    Role,
    User,
)
from stalker.models.budget import Budget, BudgetEntry, Good, Invoice, Payment, PriceList
from stalker.models.client import Client, ClientUser
from stalker.models.department import Department, DepartmentUser
from stalker.models.entity import Entity, EntityGroup, SimpleEntity
from stalker.models.format import ImageFormat
from stalker.models.file import File
from stalker.models.message import Message
from stalker.models.mixins import (
    ACLMixin,
    AmountMixin,
    CodeMixin,
    DAGMixin,
    DateRangeMixin,
    ProjectMixin,
    ReferenceMixin,
    ScheduleMixin,
    StatusMixin,
    TargetEntityTypeMixin,
    UnitMixin,
    WorkingHoursMixin,
)
from stalker.models.note import Note
from stalker.models.project import (
    Project,
    ProjectClient,
    ProjectRepository,
    ProjectUser,
)
from stalker.models.repository import Repository
from stalker.models.review import Daily, DailyFile, Review
from stalker.models.scene import Scene
from stalker.models.schedulers import SchedulerBase, TaskJugglerScheduler
from stalker.models.sequence import Sequence
from stalker.models.shot import Shot
from stalker.models.status import Status, StatusList
from stalker.models.structure import Structure
from stalker.models.studio import Studio, Vacation, WorkingHours
from stalker.models.tag import Tag
from stalker.models.task import Task, TaskDependency, TimeLog
from stalker.models.template import FilenameTemplate
from stalker.models.ticket import Ticket, TicketLog
from stalker.models.type import EntityType, Type
from stalker.models.variant import Variant
from stalker.models.version import Version
from stalker.models.wiki import Page

__all__ = [
    "ACLMixin",
    "AmountMixin",
    "Asset",
    "AuthenticationLog",
    "Budget",
    "BudgetEntry",
    "Client",
    "ClientUser",
    "CodeMixin",
    "DAGMixin",
    "Daily",
    "DailyFile",
    "DateRangeMixin",
    "Department",
    "DepartmentUser",
    "Entity",
    "EntityGroup",
    "EntityType",
    "File",
    "FilenameTemplate",
    "Good",
    "Group",
    "ImageFormat",
    "Invoice",
    "LocalSession",
    "Message",
    "Note",
    "Page",
    "Payment",
    "Permission",
    "PriceList",
    "Project",
    "ProjectClient",
    "ProjectMixin",
    "ProjectRepository",
    "ProjectUser",
    "ReferenceMixin",
    "Repository",
    "Review",
    "Role",
    "Scene",
    "ScheduleMixin",
    "SchedulerBase",
    "Sequence",
    "Shot",
    "SimpleEntity",
    "Status",
    "StatusList",
    "StatusMixin",
    "Structure",
    "Studio",
    "Tag",
    "TargetEntityTypeMixin",
    "Task",
    "TaskDependency",
    "TaskJugglerScheduler",
    "Ticket",
    "TicketLog",
    "TimeLog",
    "Type",
    "UnitMixin",
    "User",
    "Vacation",
    "Variant",
    "Version",
    "WorkingHours",
    "WorkingHoursMixin",
]


logger = log.get_logger(__name__)
