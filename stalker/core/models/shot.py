#-*- coding: utf-8 -*-



from stalker.core.models import assetBase






########################################################################
class Shot(assetBase.AssetBase):
    """Manage Shot related data.
    
    WARNING: (obviously) not implemented yet!
    
    Because most of the shots in different projects are going to have the same
    name, which is a kind of code like SH001, SH012A etc., and in Stalker you
    can not have two entities with the same name if their type is also
    matching, to guarantee all the shots are to have different names so the
    name attribute of the Shot instances are automatically set to a generated
    uuid sequence.
    
    But there is no such rule for the code attribute, which should be used to
    give shot codes to individual shots.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        kwargs["name"] = kwargs["code"] # create the test for it
        super(Shot, self).__init__(**kwargs)

