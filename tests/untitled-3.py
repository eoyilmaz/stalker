## ------- test 1 ------------
from stalker import db



db.setup()
session = db.meta.session


from stalker.core.models import tag, entity, user, department
tag1 = tag.Tag(name='tag1', description='this is the first tag')
tag2 = tag.Tag(name='tag2', description='this is the second tag')
session.add(tag1)
session.add(tag2)
session.commit()

# a new department
adminDep = department.Department(name='adminDepartment')

# a new user
admin = user.User(
    name='admin',
    description='the admin of the system',
    department=adminDep,
    email='admin@admin',
    first_name='admin',
    last_name='',
    login_name='admin'
)

adminDep.created_by = admin
adminDep.updated_by = admin

admin.created_by = admin
admin.updated_by = admin

tag1.created_by = tag1.updated_by = admin
tag2.created_by = tag2.updated_by = admin

admin.tags = [tag1, tag2]

session.add(adminDep)
session.add(admin)
session.commit()

user1 = user.User(
    name='testUser',
    login_name='testUser',
    department=adminDep,
    last_name='yilmaz',
    first_name='ozgur',
    email='eoyilmaz@gmail.com',
    created_by=admin
)

session.add(user1)
session.commit()
user1.created_by = admin
session.commit()
