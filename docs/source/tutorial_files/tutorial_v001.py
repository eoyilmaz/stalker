
from stalker import db
db.setup()

db.setup("sqlite:////tmp/studio.db")

from stalker.models import User


myUser = User(
    first_name=u"Erkan Ozgur",
    last_name=u"Yilmaz",
    login_name=u"eoyilmaz",
    email=u"eoyilmaz@gmail.com",
    password=u"secret",
    description="This is me"
)


from stalker.models import Department
tds_department = Department(name="TDs",
                            description="This is the TDs department")


tds_department.members.append(myUser)

all_departments = db.DBSession.query(Department).all()
all_members_of_dep = all_departments[0].members
print all_members_of_dep[0].first_name

db.DBSession.add(myUser)
db.DBSession.add(tds_department)

from stalker.models import Project
new_project = Project(name="Fancy Commercial")

from datetime import datetime
from stalker.models import ImageFormat

new_project.description = """The commercial is about this fancy product. The
                             client want us to have a shinny look with their
                             product bla bla bla..."""
new_project.image_format = ImageFormat(name="HD 1080", width=1920, height=1080)
new_project.fps = 25
new_project.due = datetime(2011,2,15)
new_project.lead = myUser

from stalker.models import ProjectType

commercial_project_type = ProjectType(name="Commercial")
new_project.type = commercial_project_type

db.DBSession.add(new_project)
db.DBSession.commit()


from stalker.models import Sequence
seq1 = Sequence(name="Sequence 1", code="SEQ1")

# add it to the project
new_project.sequences.append(seq1)

from stalker.models import Shot

sh001 = Shot(name="Shot 1", code="SH001")
sh002 = Shot(name="Shot 2", code="SH002")
sh003 = Shot(name="Shot 3", code="SH003")
  
# assign them to the sequence
seq1.shots.extend([sh001, sh002, sh003])


from stalker.models import PipelineStep

previs      = PipelineStep(name="Previs"     , code="PREVIS")
matchmove   = PipelineStep(name="Match Move" , code="MM")
anim        = PipelineStep(name="Animation"  , code="ANIM")
layout      = PipelineStep(name="Layout"     , code="LAYOUT")
light       = PipelineStep(name="Ligting"    , code="LIGHT")
comp        = PipelineStep(name="Compositing", code="COMP")



from stalker.models import AssetType

# the order of the PipelineSteps are not important
shot_pSteps = [previs, match, anim, layout, light, comp]

# create the asset type
shot_asset_type = AssetType(name="Shot", steps=shot_pSteps)

# and set our shot objects asset_type to shot_asset_type
# 
# instead of writing down shot1.type = shot_asset_type
# we are going to do something more interesting
# (eventhough it is inefficient)

for shot in seq1.shots:
    shot.type = shot_asset_type


from datetime import timedelta
from stalker.models import Task

previs_task = Task(
                  name="Previs",
                  resources=[myUser],
                  bid=timedelta(days=1),
                  pipeline_step=previs
              )

mm_task     = Task(
                  name="Match Move",
                  resources=[myUser],
                  bid=timedelta(days=2),
                  pipeline_step=matchmove
              )

anim_task   = Task(
                  name="Animation",
                  resources=[myUser],
                  bid=timedelta(days=2),
                  pipeline_step=anim
              )

layout_task = Task(
                  name="Layout",
                  resources=[myUser],
                  bid=timdelta(hours=2),
                  pipeline_step=layout
              )

light_task  = Task(
                  name="Lighting",
                  resources=[myUser],
                  bid=timedelta(days=2),
                  pipeline_step=light
              )

comp_task   = Task(
                  name="Compositing",
                  resources=[myUser],
                  bid=timedelta(days=2),
                  pipeline_step=comp
              )

sh001.tasks = [previs_task,
               mm_task,
               anim_task,
               layout_task,
               light_task,
               comp_task]

# animation needs match moving and previs to be finished
anim_task.depends = [mm_task, previs_task]

# compositing can not start before anything rendered or animated
comp_task.depends = [light_task, anim_task]

# lighting can not be done before the layout is finished
light_task.depends = [layout_task]


session.commit()


from stalker.models import Repository
repo1 = Repository(
    name="Commercial Repository",
    description="""This is where the commercial projects are going to be
                   stored"""
)

repo1.windows_path = "M:\\PROJECTS"
repo1.linux_path   = "/mnt/M"
repo1.osx_path     = "/Volumes/M"

print repo1.path
# outputs:
# if you are running the command on a computer with Windows it will output:
#
# M:\PROJECTS
# 
# and for Linux:
# /mnt/M 
# 
# for OSX:
# /Volumes/M
#

from stalker.models import Structure

structure1 = Structure(
    name="Commercial Projects Structure",
    description="""This is a project structure, which can be used for simple
        commercial projects"""
)

# lets create the folder structure as a Jinja2 template
project_template = """
   {{ project.code }}
   {{ project.code }}/Assets
   {{ project.code }}/Sequences"
   
   {% if project.sequences %}
       {% for sequence in project.sequences %}
           {% set seq_path = project.code + '/Sequences/' + sequence.code %}
           {{ seq_path }}
           {{ seq_path }}/Edit
           {{ seq_path }}/Edit/AnimaticStoryboard
           {{ seq_path }}/Edit/Export
           {{ seq_path }}/Storyboard
           {{ seq_path }}/Shots
           
           {% if sequence.shots %}
               {% for shot in sequence.shots %}
                   {% set shot_path = seq_path + '/SHOTS/' + shot.code %}
                   {{ shot_path }}
               {% endfor %}
           {% endif %}
           
       {% endfor %}
   
   {% endif %}
   
   {{ project.code }}/References
"""

structure1.project_template = project_template


#M:/PROJECTS/FANCY_COMMERCIAL
#M:/PROJECTS/FANCY_COMMERCIAL/Assets
#M:/PROJECTS/FANCY_COMMERCIAL/References
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit/AnimaticStoryboard
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit/Export
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Storyboard
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH001
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH002
#M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH003

