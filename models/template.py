#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Template(entity.SimpleEntity):
    """This is the template model. It holds templates for various tasks. The
    only attribute it has is the `template_code` attiribute
    
    :param template_code: holds the template code suitable to the template
    engine selected in the settings, the default template rendering engine is
    Jinja2, so the code is should be a jinja2 template if you want to use the
    defaults. It should be a string or unicode value, and cannot be empty
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, template_code, **kwargs):
        super(Template, self).__init__(**kwargs)
        
        self._template_code = self._check_template_code(template_code)
    
    
    
    #----------------------------------------------------------------------
    def _check_template_code(self, template_code_in):
        """checks the given template_code attribute for several conditions
        """
        
        # check if it is None
        if template_code_in is None:
            raise(ValueError('template_code could not be None'))
        
        # check if it is an empty string
        if template_code_in == "":
            raise(ValueError('template_code could not be an empty string'))
        
        # check if it is an instance of string or unicode
        if not isinstance(template_code_in, (str, unicode)):
            raise(ValueError('template_code should be an instance of string \
            or unicode'))
        
        return template_code_in
    
    
    
    #----------------------------------------------------------------------
    def template_code():
        
        def fget(self):
            return self._template_code
        
        def fset(self, template_code_in):
            self._template_code = self._check_template_code(template_code_in)
        
        doc = """this is the property that helps you assign values to
        template_code attribute"""
        
        return locals()
    
    template_code = property(**template_code())
    
    
    