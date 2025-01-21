# -*- coding: utf-8 -*-
import stalker.db.setup
from stalker import db
from stalker.db.session import DBSession
from stalker import (
    Asset,
    FilenameTemplate,
    ImageFormat,
    Repository,
    Project,
    Shot,
    Structure,
    Task,
    Type,
    User,
    Version,
)
from stalker.models.enum import TimeUnit


def test_readme_tutorial_code(setup_sqlite3):
    """the tutorial code in README.rst."""
    stalker.db.setup.setup()
    stalker.db.setup.init()

    assert str(DBSession.connection().engine.url) == "sqlite://"

    me = User(
        name="Erkan Ozgur Yilmaz",
        login="erkanozgur",
        email="my_email@gmail.com",
        password="secretpass",
    )

    # Save the user to database
    DBSession.save(me)

    repo = Repository(
        name="Commercial Projects Repository",
        code="CPR",
        windows_path="Z:/Projects",
        linux_path="/mnt/Z/Projects",
        macos_path="/Volumes/Z/Projects",
    )

    task_template = FilenameTemplate(
        name="Standard Task Filename Template",
        target_entity_type="Task",  # This is for files saved for Tasks
        path="{{project.repository.path}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",  # This is Jinja2 template code
        filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}',
    )

    standard_folder_structure = Structure(
        name="Standard Project Folder Structure",
        templates=[task_template],
        custom_template="{{project.code}}/References",  # If you need extra folders
    )

    new_project = Project(
        name="Test Project",
        code="TP",
        structure=standard_folder_structure,
        repositories=[repo],  # if you have more than one repository you can do it
    )

    hd1080 = ImageFormat(name="1080p", width=1920, height=1080)

    new_project.image_format = hd1080

    # Save the project and all the other data it is connected to it
    DBSession.save(new_project)

    # define Character asset type
    char_type = Type(name="Character", code="CHAR", target_entity_type="Asset")

    character1 = Asset(
        name="Character 1", code="CHAR1", type=char_type, project=new_project
    )

    # Save the Asset
    DBSession.save(character1)

    model = Task(name="Model", parent=character1)

    rigging = Task(
        name="Rig",
        parent=character1,
        depends_on=[model],  # For project management, define that Rig cannot start
        # before Model ends.
    )

    # Save the new tasks
    DBSession.save([model, rigging])

    # A shot and some tasks for it
    shot = Shot(name="SH001", code="SH001", project=new_project)

    # Save the Shot
    DBSession.save(shot)

    animation = Task(
        name="Animation",
        parent=shot,
    )

    lighting = Task(
        name="Lighting",
        parent=shot,
        depends_on=[animation],  # Lighting cannot start before Animation ends,
        schedule_timing=1,
        schedule_unit=TimeUnit.Day,  # The task expected to take 1 day to complete
        resources=[me],
    )
    DBSession.save([animation, lighting])

    new_version = Version(task=animation)
    new_version.generate_path()  # to render the naming convention template
    new_version.extension = ".ma"  # let's say that we have created under Maya
    DBSession.save(new_version)

    path = new_version.generate_path(extension=".ma")
    assert str(path) == f"{repo.path}TP/SH001/Animation/SH001_Animation_v001.ma"
    assert new_version.version_number == 1

    new_version2 = Version(task=animation)
    DBSession.save(new_version2)

    # to render the naming convention template
    # let's say that we have created under Maya
    # path = new_version2.generate_path(extension = ".ma")
    assert new_version2.version_number == 2
