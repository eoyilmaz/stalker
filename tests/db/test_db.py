# ------- test 1 ------------
from stalker import db



db.setup()
session = db.meta.session


#from stalker.models import tag, entity
#tag1 = tag.Tag(name='tag1', description='this is the first tag')
#tag2 = tag.Tag(name='tag2', description='this is the second tag')
#session.add(tag1)
#session.add(tag2)
#session.commit()

## create a tagged entity
#aTaggedEntity1 = entity.TaggedEntity(name='taggedEntity1', description='test')

#aTaggedEntity1.tags = [tag1, tag2]

#session.add(aTaggedEntity1)
#session.commit()


## a new user


#for aTag in session.query(tag.Tag).all():
    #print aTag.name


