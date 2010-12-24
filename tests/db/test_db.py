# ------- test 1 ------------
from stalker.db import setup_db, meta
setup_db.do_setup()

session = meta.session

from stalker.models import tag
tag1 = tag.Tag(name='tag1', description='this is the first tag')
tag2 = tag.Tag(name='tag2', description='this is the second tag')
session.add(tag1)
session.add(tag2)
session.commit()


for aTag in session.query(tag.Tag).all():
    print aTag.name

