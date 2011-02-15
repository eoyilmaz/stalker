#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin
from stalker.ext.validatedList import ValidatedList






########################################################################
class Sequence(entity.Entity, mixin.ReferenceMixin, mixin.StatusMixin,
               mixin.ScheduleMixin):
    """Stores data about Sequences.
    
    Sequences are holders of the :class:`~stalker.core.models.shot.Shot`
    objects. They orginize the conceptual data with another level of
    complexity.
    
    :param project: The :class:`~stalker.core.models.project.Project` that this
      Sequence belongs to. The default value is None.
    
    :type project: :class:`~stalker.core.models.project.Project`.
    
    :param list shots: The list of :class:`~stalker.core.models.shot.Shot`
      objects that this Sequence has. The default value is an empty list.
    
    :param lead: The lead of this Seuqence. The default value is None.
    
    :type lead: :class:`~stalker.core.models.user.User`
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 project=None,
                 shots=[],
                 lead=None,
                 **kwargs
                 ):
        
        super(Sequence, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        mixin.ReferenceMixin.__init__(self, **kwargs)
        mixin.StatusMixin.__init__(self, **kwargs)
        mixin.ScheduleMixin.__init__(self, **kwargs)
        
        self._project = self._validate_project(project)
        self._lead = self._validate_lead(lead)
        self._shots = self._validate_shots(shots)
    
    
    
    #----------------------------------------------------------------------
    def _validate_project(self, project_in):
        """validates the given project_in value
        """
        
        from stalker.core.models.project import Project
        
        if project_in is not None:
            if not isinstance(project_in, Project):
                raise ValueError("project should be instance of"
                                 "stalker.core.models.project.Project")
        
        return project_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        from stalker.core.models.user import User
        
        if lead_in is not None:
            if not isinstance(lead_in, User):
                raise ValueError("lead should be instance of "
                                 "stalker.core.models.user.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_shots(self, shots_in):
        """validates the given shots_in value
        """
        
        from stalker.core.models.shot import Shot
        
        if shots_in is None:
            shots_in = []
        
        if not isinstance(shots_in, list):
            raise ValueError("shots should be list containing "
                             "stalker.core.models.shot.Shot instances")
        
        for element in shots_in:
            if not isinstance(element, Shot):
                raise ValueError("every item in the shots list should be an "
                                 "instance of stalker.core.models.shot.Shot")
        
        return ValidatedList(shots_in, Shot)
        
    
    
    
    #----------------------------------------------------------------------
    def project():
        def fget(self):
            return self._project
        def fset(self, project_in):
            self._project = self._validate_project(project_in)
        
        doc ="""The Project of this sequence object."""
        
        return locals()
    
    project = property(**project())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        def fget(self):
            return self._lead
        def fset(self, lead_in):
            self._lead = self._validate_lead(lead_in)
        
        doc = """The lead of this sequence object."""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def shots():
        def fget(self):
            return self._shots
        def fset(self, shots_in):
            self._shots = self._validate_shots(shots_in)
        
        doc = """The shots of this sequence object."""
        
        return locals()
    
    shots = property(**shots())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Sequence, self).__eq__(other) and \
               isinstance(other, Sequence)
    
    
    