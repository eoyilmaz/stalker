#-*- coding: utf-8 -*-
"""This contains little utility functions, like string conditioning etc.
"""




#----------------------------------------------------------------------
def path_to_exec(full_module_path):
    """This is a utiliy function which converts full class or function paths
    to python executable import commands, the result is a tuple where the
    first element is the command, the second is the module and the third is the
    object names::
      
      from stalker import utils
      
      full_path = "stalker.core.models.asset.Asset"
      
      command = utils.path_to_exec(full_path)
      
      print command
      
      # will print the result
      # ("from stalker.core.models.asset import Asset",
      #  "stalker.core.models.asset",
      #  "Asset")
    
    """
    
    splits = full_module_path.split(".")
    
    module = ".".join(splits[:-1])
    object_ = splits[-1]
    exec_ = "from %s import %s" % (module, object_)
    
    return (exec_, module, object_)



