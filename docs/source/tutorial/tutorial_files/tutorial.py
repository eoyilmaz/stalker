# -*- coding: utf-8 -*-

import os

import stalker.db.setup

stalker.db.setup.setup({"sqlalchemy.url": "sqlite:///"})
stalker.db.setup.init()


from stalker import Studio

my_studio = Studio(name="My Great Studio")

from stalker import User

me = User(
    name="Erkan Ozgur Yilmaz",
    login="eoyilmaz",
    email="some_email_address@gmail.com",
    password="secret",
    description="This is me",
)

from stalker import Department

tds_department = Department(name="TDs", description="This is the TDs department")

tds_department.users.append(me)

print(me.departments)
# you should get something like
# [<TDs (Department)>]


from stalker.db.session import DBSession

DBSession.add(my_studio)
DBSession.add(me)
DBSession.add(tds_department)
DBSession.commit()


all_departments = Department.query.all()
print(all_departments)
# This should print something like
# [<admins (Department)>, <TDs (Department)>]
# "admins" department is created by default

admins = all_departments[0]
tds = all_departments[1]

all_users = tds.users  # Department.users is a synonym for Department.members
# they are essentially the same attribute
print(all_users[0])
# this should print
# <Erkan Ozgur Yilmaz ('eoyilmaz') (User)>

# we will reuse the Statuses created by default (in db.init())
from stalker import Status

status_new = Status.query.filter_by(code="NEW").first()
status_wip = Status.query.filter_by(code="WIP").first()
status_cmpl = Status.query.filter_by(code="CMPL").first()

# a status list which is suitable for Project instances
from stalker import StatusList, Project

project_statuses = StatusList(
    name="Project Status List",
    statuses=[status_new, status_wip, status_cmpl],
    target_entity_type="Project"  # you can also use Project which is the
    # class itself
)

from stalker import Repository

# and the repository itself
commercial_repo = Repository(name="Commercial Repository", code="CR")

new_project = Project(
    name="Fancy Commercial",
    code="FC",
    status_list=project_statuses,
    repositories=[commercial_repo],
)

import tzlocal
import datetime
from stalker import ImageFormat

new_project.description = """The commercial is about this fancy product. The
client want us to have a shiny look with their
product bla bla bla..."""

new_project.image_format = ImageFormat(name="HD 1080", width=1920, height=1080)

new_project.fps = 25
local_tz = tzlocal.get_localzone()
new_project.end = datetime.datetime(2014, 5, 15, tzinfo=local_tz)
new_project.users.append(me)

DBSession.add(new_project)
DBSession.commit()

from stalker import Sequence

seq1 = Sequence(
    name="Sequence 1",
    code="SEQ1",
    project=new_project,
)

from stalker import Shot

sh001 = Shot(name="SH001", code="SH001", project=new_project, sequences=[seq1])
sh002 = Shot(code="SH002", project=new_project, sequences=[seq1])
sh003 = Shot(code="SH003", project=new_project, sequences=[seq1])

DBSession.add_all([sh001, sh002, sh003])
DBSession.commit()

sh004 = Shot(code="SH004", project=new_project, sequences=[seq1])
DBSession.add(sh004)
DBSession.commit()

sh004.code = "SH005"
DBSession.commit()

# first find the data
wrong_shot = Shot.query.filter_by(code="SH005").first()

# now update it
wrong_shot.code = "SH004"

# commit the changes to the database
DBSession.commit()

DBSession.delete(wrong_shot)
DBSession.commit()

wrong_shot = Shot.query.filter_by(code="SH005").first()
print(wrong_shot)
# should print None

from stalker import Task

previs = Task(name="Previs", parent=sh001)

matchmove = Task(name="Matchmove", parent=sh001)

anim = Task(name="Animation", parent=sh001)

lighting = Task(name="Lighting", parent=sh001)

comp = Task(name="comp", parent=sh001)

comp.depends_on = [lighting]
lighting.depends_on = [anim]
anim.depends_on = [previs, matchmove]

previs.resources = [me]
previs.schedule_timing = 10
previs.schedule_unit = "d"

matchmove.resources = [me]
matchmove.schedule_timing = 2
matchmove.schedule_unit = "d"

anim.resources = [me]
anim.schedule_timing = 5
anim.schedule_unit = "d"

lighting.resources = [me]
lighting.schedule_timing = 3
lighting.schedule_unit = "d"

comp.resources = [me]
comp.schedule_timing = 6
comp.schedule_unit = "h"

DBSession.commit()

from stalker import TaskJugglerScheduler

my_studio.scheduler = TaskJugglerScheduler()
my_studio.duration = datetime.timedelta(days=365)  # we are setting the
my_studio.schedule(scheduled_by=me)  # duration to 1 year just
# to be sure that TJ3
# will not complain
# about the project is not
# fitting in to the time
# frame.

DBSession.commit()  # to reflect the change

print(previs.computed_start)  # 2014-04-02 16:00:00
print(previs.computed_end)  # 2014-04-15 15:00:00

print(matchmove.computed_start)  # 2014-04-15 15:00:00
print(matchmove.computed_end)  # 2014-04-17 13:00:00

print(anim.computed_start)  # 2014-04-17 13:00:00
print(anim.computed_end)  # 2014-04-23 17:00:00

print(lighting.computed_start)  # 2014-04-23 17:00:00
print(lighting.computed_end)  # 2014-04-24 11:00:00

print(comp.computed_start)  # 2014-04-24 11:00:00
print(comp.computed_end)  # 2014-04-24 17:00:00

print(my_studio.to_tjp)
print(me.to_tjp)
print(comp.to_tjp)
print(new_project.to_tjp)

commercial_repo.linux_path = "/mnt/M/commercials"
commercial_repo.macos_path = "/Volumes/M/commercials"
commercial_repo.windows_path = "M:/commercials"  # you can use reverse slashes
# (\\) if you want

print(commercial_repo.path)
# under Windows outputs:
# M:/commercials
#
# in Linux and variants:
# /mnt/M/commercials
#
# and in macOS:
# /Volumes/M/commercials


from stalker import Structure

commercial_project_structure = Structure(name="Commercial Projects Structure")

# now assign this structure to our project
new_project.structure = commercial_project_structure

from stalker import FilenameTemplate

task_template = FilenameTemplate(
    name="Task Template for Commercials",
    target_entity_type="Task",
    path="$REPO{{project.repository.id}}/{{project.code}}/{%- for p in parent_tasks -%}{{p.nice_name}}/{%- endfor -%}",
    filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}',
)

# and append it to our project structure
commercial_project_structure.templates.append(task_template)

# commit to database
DBSession.commit()  # no need to add anything, project is already on db

from stalker import Version

vers1 = Version(task=comp)

# we need to update the paths
path = vers1.generate_path()

# check the path and filename
print(path.parent)  # '$REPO33/FC/SH001/comp'
print(path.name)  # 'SH001_comp_Main_v001'
print(path)  # '$REPO33/FC/SH001/comp/SH001_comp_Main_v001'
# now the absolute values, values with repository root
# because I'm running this code in a Linux laptop, my results are using the
# linux path of the repository
print(vers1.absolute_path)  # '/mnt/M/commercials/FC/SH001/comp'
print(
    vers1.absolute_full_path
)  # '/mnt/M/commercials/FC/SH001/comp/SH001_comp_Main_v001'

# check the version_number
print(vers1.version_number)  # 1

# commit to database
DBSession.commit()

vers1.is_published = False  # I still work on this version, this is not a
# usable one

# be sure that you've committed the previous version to the database
# to let Stalker now what number to give for the next version
vers2 = Version(task=comp)
vers2.generate_path()  # this call probably will disappear in next version of
# Stalker, so Stalker will automatically update the
# paths on Version.__init__()

print(vers2.version_number)  # 2
print(vers2.filename)  # 'SH001_comp_Main_v002'

# before creating a new version commit this one to db
DBSession.commit()

# now create a new version
vers3 = Version(task=comp)
vers3.generate_path()

print(vers3.version_number)  # 3
print(vers3.filename)  # 'SH001_comp_Main_v002'

# using pure Python
vers_from_python = comp.versions  # [<FC_SH001_comp_Main_v001 (Version)>,
#  <FC_SH001_comp_Main_v002 (Version)>,
#  <FC_SH001_comp_Main_v003 (Version)>]

# or using a query
vers_from_query = Version.query.filter_by(task=comp).all()

# again returns
# [<FC_SH001_comp_Main_v001 (Version)>,
#  <FC_SH001_comp_Main_v002 (Version)>,
#  <FC_SH001_comp_Main_v003 (Version)>]

assert vers_from_python == vers_from_query

commercial_project_structure.custom_template = """
Temp
References
References/Movies
References/Images
"""
