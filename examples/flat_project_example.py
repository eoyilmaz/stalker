# -*- coding: utf-8 -*-
"""This is an example which uses two different folder structure in two
different projects.

The first one prefers to use a flat one, in which all the files are in the same
folder.

The second project uses a more traditional folder structure where every
Task/Asset/Shot/Sequence has its own folder and the Task hierarchy is directly
reflected to folder hierarchy.
"""

from stalker import (db, Project, Repository, Structure, FilenameTemplate,
                     Task, Status, StatusList, Version, Sequence, Shot)

# initialize an in memory sqlite3 database
db.setup()

# fill in default data
db.init()

# create a new repository
repo = Repository(
    name='Test Repository',
    linux_path='/mnt/T/stalker_tests/',
    osx_path='/Volumes/T/stalker_tests/',
    windows_path='T:/stalker_tests/'
)

# create a Structure for our flat project
flat_task_template = FilenameTemplate(
    name='Flat Task Template',
    target_entity_type='Task',
    path='{{project.code}}',  # everything will be under the same folder
    filename='{{task.nice_name}}_{{version.take_name}}'
             '_v{{"%03d"|format(version.version_number)}}{{extension}}'
             # you can customize this as you wish, you can even use a uuid4
             # as the file name
)

flat_struct = Structure(
    name='Flat Project Structure',
    templates=[flat_task_template]  # we need another template for Assets,
                                    # Shots and Sequences but I'm skipping it
                                    # for now
)

# query a couple of statuses
status_new = Status.query.filter_by(code='NEW').first()
status_wip = Status.query.filter_by(code='WIP').first()
status_cmpl = Status.query.filter_by(code='CMPL').first()

proj_statuses = StatusList(
    name='Project Statuses',
    target_entity_type='Project',
    statuses=[status_new, status_wip, status_cmpl]
)

p1 = Project(
    name='Flat Project Example',
    code='FPE',
    status_list=proj_statuses,
    repository=repo,
    structure=flat_struct
)

# now lets create a Task
t1 = Task(name='Building 1', project=p1)
t2 = Task(name='Model', parent=t1)
t3 = Task(name='Lighting', parent=t1, depends=[t2])

# store all the data in the database
db.DBSession.add_all([t1, t2, t3])  # this is enough to store the rest


# lets create a Maya file for the Model task
t2_v1 = Version(task=t1)
t2_v1.update_paths()  # for now this is needed to render the template, but will
                   # remove it later on
t2_v1.extension = '.ma'  # set the extension for maya

# lets create a new version for Lighting
t3_v1 = Version(task=t3)
t3_v1.update_paths()
t3_v1.extension = '.ma'

# you should see that all are in the same folder
print(t2_v1.absolute_full_path)
print(t3_v1.absolute_full_path)

#
# Lets create a second Project that use some other folder structure
#

# create a new project structure
normal_task_template = FilenameTemplate(
    name='Flat Task Template',
    target_entity_type='Task',
    path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
         '{{parent_task.nice_name}}/{%- endfor -%}',  # all in different folder
    filename='{{task.nice_name}}_{{version.take_name}}'
             '_v{{"%03d"|format(version.version_number)}}{{extension}}'
)

# we will use sequences and shots in this project so lets define a template
# for each of the types

# because we will use Sequences, Shots and Assets for this type of projects
# we need to supply a new FilenameTemplate for each type (we will not do it
# again for other new projects that will use this structure).
#
# Also, we can use the same template variables from the normal_task_template
seq_template = FilenameTemplate(
    name='Sequence Template',
    target_entity_type='Sequence',
    path=normal_task_template.path,
    filename=normal_task_template.filename
)
shot_template = FilenameTemplate(
    name='Shot Template',
    target_entity_type='Shot',
    path=normal_task_template.path,
    filename=normal_task_template.filename
)
asset_template = FilenameTemplate(
    name='Asset Template',
    target_entity_type='Asset',
    path=normal_task_template.path,
    filename=normal_task_template.filename
)

normal_struct = Structure(
    name='Normal Project Structure',
    templates=[
        normal_task_template,
        seq_template,
        shot_template,
        asset_template
    ]
)

p2 = Project(
    name='Normal Project Example',
    code='NPE',
    status_list=proj_statuses,
    repository=repo,  # can be freely in the same repo
    structure=normal_struct  # but uses a different structure
)

# now create new tasks for the normal project
seq1 = Sequence(name='Sequence', code='SEQ001', project=p2)
shot1 = Shot(name='SEQ001_0010', code='SEQ001_0010', parent=seq1,
             sequences=[seq1])
comp = Task(name='Comp', parent=shot1)
# you probably will supply a different name/code

# it is a good idea to commit the data now
db.DBSession.add(shot1)  # this should be enough to add the rest

# now create new maya files for them
comp_v1 = Version(task=comp, take_name='Test')
comp_v1.update_paths()
comp_v1.extension = '.ma'

print(comp_v1.absolute_full_path)  # as you see it is in a proper shot folder
