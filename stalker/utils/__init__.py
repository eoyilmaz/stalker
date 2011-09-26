#-*- coding: utf-8 -*-
"""This contains little utility functions, like string conditioning etc.
"""


def path_to_exec(full_module_path):
    """This is a utiliy function which converts full class or function paths
    to python executable import commands, the result is a tuple where the
    first element is the command, the second is the module and the third is the
    object names::
      
      from stalker import utils
      
      full_path = "stalker.core.models.Asset"
      
      command = utils.path_to_exec(full_path)
      
      print command
      
      # will print the result
      # ("from stalker.core.models import Asset",
      #  "stalker.core.models.asset",
      #  "Asset")
    
    """

    splits = full_module_path.split(".")

    module = ".".join(splits[:-1])
    object_ = splits[-1]
    exec_ = "from %s import %s" % (module, object_)

    return (exec_, module, object_)


def Property(func):
    """A convenient way of using property
    
    taken from:
    http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
    """

    locals_ = func()

    # update the docs with the func doc
    if func.__doc__ is not None:
    #print "updating the doc ('%s')for %s with %s" % \
    #(locals_["doc"], func.__name__, func.__doc__)
        locals_.update({"doc": func.__doc__})

    return property(**locals_)
