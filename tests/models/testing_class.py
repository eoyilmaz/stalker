class AClass(object):
    def __init__(self,
                 arg1=None,
                 arg2=None):
        print arg1, arg2

class BClass(AClass):
    def __init__(self,
                 arg3=None,
                 arg4=None,
                 **kwargs):
        super(BClass,self).__init__(**kwargs)
        print arg3, arg4

