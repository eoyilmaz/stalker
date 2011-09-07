from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

# The Base Class
########################################################################
class SimpleEntity(Base):
    __tablename__ = "SimpleEntities"
    id = Column("id", Integer, primary_key=True)
    
    entity_type = Column("db_entity_type", String(128), nullable=False)
    __mapper_args__ = {
        "polymorphic_on": entity_type,
        "polymorphic_identity": "SimpleEntity",
    }
    
    name = Column(String(256), nullable=False)
    
    #----------------------------------------------------------------------
    def __init__(self, name=None, **kwargs):
        
        self.name = name

########################################################################
class Task(SimpleEntity):
    __tablename__ = "Tasks"
    task_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                     primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "Task",
                       "inherit_condition": task_id==SimpleEntity.id}
    
    task_of_id = Column(Integer,
                        ForeignKey("SimpleEntities.id")
                        )
    
    #----------------------------------------------------------------------
    def __init__(self, task_of=None, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.task_of = task_of

########################################################################
class TaskMixin(object): # The mixin
    def __init__(self, tasks=None, **kwargs):
        if tasks is None:
            tasks = []
        self.tasks = tasks
    
    #----------------------------------------------------------------------
    @declared_attr
    def tasks(cls):
        return relationship(
            "Task",
            primaryjoin="Tasks.c.task_of_id==SimpleEntities.c.id",
            backref="task_of",
        )


########################################################################
# example class 1 - defining only one class with TaskMixin doesn't create
# any problem
class TaskableClassA(SimpleEntity, TaskMixin):
    __tablename__ = "TaskableAs"
    __mapper_args__ = {"polymorphic_identity": "TaskableClassA"}
    taskableClass_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                              primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        TaskMixin.__init__(self, **kwargs)

#######################################################################
# example class 2 - which creates the problem
class TaskableClassB(SimpleEntity, TaskMixin):
    __tablename__ = "TaskableBs"
    __mapper_args__ = {"polymorphic_identity": "TaskableClassB"}
    taskableClass_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                              primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        TaskMixin.__init__(self, **kwargs)

a_taskable_object = TaskableClassA(name="taskable test object")
task1 = Task(name="Test Task1", task_of=a_taskable_object)