#-*- coding: utf-8 -*-


import datetime
from stalker.core.models import (entity, mixin, asset, imageFormat, user,
                                 repository, sequence, structure, types)
from stalker.ext.validatedList import ValidatedList






########################################################################
class Project(entity.Entity, mixin.ReferenceMixin, mixin.StatusMixin,
              mixin.ScheduleMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    It is mixed with :class:`~stalker.core.models.mixin.ReferenceMixin`,
    :class:`~stalker.core.models.mixin.StatusMixin` and
    :class:`~stalker.core.models.mixin.ScheduleMixin` to give reference, status
    and schedule abilities.
    
    :param lead: The lead of the project. Default value is None.
    
    :type lead: :class:`~stalker.core.models.user.User`
    
    :param list users: The users assigned to this project, should be a list of
      :class:`~stalker.core.models.user.User` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param list sequences: The sequences of the project, it should be a list of
      :class:`~stalker.core.models.sequence.Sequence` instances, if set to None
      it is converted to an empty list. Default value is an empty list.
    
    :param list assets: The assets used in this project, it should be a list of
      :class:`~stalker.core.models.asset.Asset` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param image_format: The output image format of the project. Default
      value is None.
    
    :type image_format: :class:`~stalker.core.models.imageFormat.ImageFormat`
    
    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.
    
    :param type: The type of the project. Default value is None.
    
    :type type: :class:`~stalker.core.models.types.ProjectType`
    
    :param structure: The structure of the project. Default value is None
    
    :type structure: :class:`~stalker.core.models.structure.Structure`
    
    :param repository: The repository that the project files are going to be
      stored in. You can not create the project folder structure if the project
      doesn't have a connection to a
      :class:`~stalker.core.models.repository.Repository`. Default value is
      None.
    
    :type repository: :class:`~stalker.core.models.repository.Repository`.
    
    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.
    
    :param float display_width: the width of the display that the output of the
      project is going to be displayed (very unnecessary if you are not using
      stereo 3D setup). Should be an int or float value, negative values
      converted to the positive values. Default value is 1.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=datetime.date.today(),
                 due_date=datetime.timedelta(days=10),
                 lead=None,
                 users=[],
                 repository=None,
                 type=None,
                 structure=None,
                 sequences=[],
                 assets=[],
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 display_width=1.0,
                 references=[],
                 **kwargs):
        
        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        mixin.ReferenceMixin.__init__(self, **kwargs)
        mixin.StatusMixin.__init__(self, **kwargs)
        mixin.ScheduleMixin.__init__(self, **kwargs)
        
        self._start_date = self._validate_start_date(start_date)
        self._due_date = self._validate_due_date(due_date)
        self._lead = self._validate_lead(lead)
        self._users = self._validate_users(users)
        self._repository = self._validate_repository(repository)
        self._type = self._validate_type(type)
        self._structure = self._validate_structure(structure)
        self._sequences = self._validate_sequences(sequences)
        self._assets = self._validate_assets(assets)
        
        # do not persist this attribute
        self._project_duration = self._due_date - self._start_date
        
        self._image_format = self._validate_image_format(image_format)
        self._fps = self._validate_fps(fps)
        self._is_stereoscopic = bool(is_stereoscopic)
        self._display_width = self._validate_display_width(display_width)
        
        ## update the mixin side of the project class (status and references)
        #self.status_list = status_list
        #self.status = status
        #self.references = references
        #self.start_date = start_date
        #self.due_date = due_date
    
    
    
    #----------------------------------------------------------------------
    def _validate_assets(self, assets_in):
        """validates the given assets_in lists
        """
        
        if assets_in is None:
            assets_in = []
        
        if not all([isinstance(element, asset.Asset)
                    for element in assets_in]):
            raise ValueError("the elements in assets lists should be all "
                             "stalker.core.models.asset.Asset instances")
        
        return ValidatedList(assets_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_display_width(self, display_width_in):
        """validates the given display_width_in value
        """
        
        return abs(float(display_width_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_fps(self, fps_in):
        """validates the given fps_in value
        """
        
        fps_in = float(fps_in)
        
        return fps_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_image_format(self, image_format_in):
        """validates the given image format
        """
        
        if image_format_in is not None and \
           not isinstance(image_format_in, imageFormat.ImageFormat):
            raise ValueError("the image_format should be an instance of "
                             "stalker.core.models.imageFormat.ImageFormat")
        
        return image_format_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        if lead_in is not None:
            if not isinstance(lead_in, user.User):
                raise ValueError("lead must be an instance of "
                                 "stalker.core.models.user.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_repository(self, repository_in):
        """validates the given repository_in value
        """
        
        if repository_in is not None and \
           not isinstance(repository_in, repository.Repository):
            raise ValueError("the repsoitory should be an instance of "
                             "stalker.core.models.repository.Repository")
        
        return repository_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences(self, sequences_in):
        """validates the given sequences_in value
        """
        
        if sequences_in is None:
            sequences_in = []
        
        if not all([isinstance(seq, sequence.Sequence)
                    for seq in sequences_in]):
            raise ValueError("sequences should be a list of "
                             "stalker.core.models.sequence.Sequence instances")
        
        return ValidatedList(sequences_in, sequence.Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_structure(self, structure_in):
        """validates the given structure_in vlaue
        """
        
        if structure_in is not None:
            if not isinstance(structure_in, structure.Structure):
                raise ValueError("structure should be an instance of "
                                 "stalker.core.models.structure.Structure")
        
        return structure_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type_in value
        """
        
        if type_in is not None and not isinstance(type_in, types.ProjectType):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.types.ProjectType")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_users(self, users_in):
        """validates the given users_in value
        """
        
        if users_in is None:
            users_in = []
        
        if not all([isinstance(element, user.User) \
                    for element in users_in]):
            raise ValueError("users should be a list containing instances of "
                             ":class:`~stalker.core.models.user.User`")
        
        return ValidatedList(users_in)
    
    
    
    #----------------------------------------------------------------------
    def assets():
        def fget(self):
            return self._assets
        
        def fset(self, assets_in):
            self._assets = self._validate_assets(assets_in)
        
        doc = """the list of assets created in this project"""
        
        return locals()
    
    assets = property(**assets())
    
    
    
    #----------------------------------------------------------------------
    def display_width():
        def fget(self):
            return self._display_width
        
        def fset(self, display_width_in):
            self._display_width = \
                self._validate_display_width(display_width_in)
        
        doc = """the target display width that this project is going to be
        displayed on, meaningfull if this project is a stereoscopic project"""
        
        return locals()
    
    display_width = property(**display_width())
    
    
    
    #----------------------------------------------------------------------
    def fps():
        def fget(self):
            return self._fps
        def fset(self, fps_in):
            self._fps = self._validate_fps(fps_in)
        
        doc = """the fps of the project, it is a float value, any other types
        will be converted to float. The default value is 25.0"""
        
        return locals()
    
    fps = property(**fps())
    
    
    
    #----------------------------------------------------------------------
    def image_format():
        def fget(self):
            return self._image_format
        def fset(self, image_format_in):
            self._image_format = \
                self._validate_image_format(image_format_in)
        
        doc = """the image format of the current project. This value defines
        the output image format of the project, should be an instance of
        :class:`~stalker.core.models.imageFormat.ImageFormat`, can not be
        skipped"""
        
        return locals()
    
    image_format = property(**image_format())
    
    
    
    #----------------------------------------------------------------------
    def is_stereoscopic():
        def fget(self):
            return self._is_stereoscopic
        def fset(self, is_stereoscopic_in):
            self._is_stereoscopic = bool(is_stereoscopic_in)
        
        doc= """True if the project is a stereoscopic project"""
        
        return locals()
    
    is_stereoscopic = property(**is_stereoscopic())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        def fget(self):
            return self._lead
        def fset(self, lead_in):
            self._lead = self._validate_lead(lead_in)
        
        doc = """the lead of the project, should be an instance of
        :class:`~stalker.core.models.user.User`, also can set to None"""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def repository():
        def fget(self):
            return self._repository
        def fset(self, repository_in):
            self._repository = self._validate_repository(repository_in)
        
        doc = """the repository that this project should reside, should be an
        instance of :class:`~stalker.core.models.repository.Repository`, can
        not be skipped"""
        
        return locals()
    
    repository = property(**repository())
    
    
    
    #----------------------------------------------------------------------
    def sequences():
        def fget(self):
            return self._sequences
        def fset(self, sequences_in):
            self._sequences = self._validate_sequences(sequences_in)
        
        doc = """the sequences contained in this project, should be a list
        containing all of :class:`~stalker.core.models.sequence.Sequence`
        instances, when set to None it is converted to an empty list"""
        
        return locals()
    
    sequences = property(**sequences())
    
    
    
    #----------------------------------------------------------------------
    def structure():
        def fget(self):
            return self._structure
        def fset(self, structure_in):
            self._structure = self._validate_structure(structure_in)
        
        doc = """The structure of the project. Should be an instance of
        :class:`~stalker.core.models.structure.Structure` class"""
        
        return locals()
    
    structure = property(**structure())
    
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """defines the type of the project, should be an instance of
        :class:`~stalker.core.models.types.ProjectType`"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def users():
        def fget(self):
            return self._users
        def fset(self, users_in):
            self._users = self._validate_users(users_in)
        
        doc = """the users assigned to this project. Should be a list of
        :class:`~stalker.core.models.user.User` instances. Can be and empty
        list, and when set to None it will be converted to an empty list"""
        
        return locals()
    
    users = property(**users())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Project, self).__eq__(other) and \
               isinstance(other, Project)
    
    
    