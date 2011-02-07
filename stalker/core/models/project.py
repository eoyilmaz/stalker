#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin






########################################################################
class Project(entity.Entity, mixin.ReferenceMixin, mixin.StatusMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    The date attributes like start_date and due_date can be managed with
    timezones. Follow the Python idioms shown in the `help files of datetime`_
    
    .. _help files of datetime: http://docs.python.org/library/datetime.html
    
    It is mixed with :class:`~stalker.core.models.mixin.ReferenceMixin` and
    :class:`~stalker.core.models.mixin.StatusMixin` to give reference and
    status abilities.
    
    
    :param start_date: the start date of the project, should be a datetime.date
      instance, when given as None or tried to be set to None, it is to set to
      today, setting the start date also effects due date, if the new
      start_date passes the due_date the due_date is also changed to a date to
      keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :param due_date: the due_date of the project, should be a datetime.date or
      datetime.timedelta instance, if given as a datetime.timedelta, then it
      will be converted to date by adding the timedelta to the start_date
      attribute, when the start_date is changed to a date passing the due_date,
      then the due_date is also changed to a later date so the timedelta is
      kept between the dates. The default value is 10 days given as
      datetime.timedelta
    
    :param lead: the lead of the project, should be an instance of
      :class:`~stalker.core.models.user.User`
    
    :param users: the users assigned to this project, should be a list of
      :class:`~stalker.core.models.user.User` instances, if set to None it is
      converted to an empty list.
    
    :param sequences: the sequences of the project, it should be a list of
      :class:`~stalker.core.models.sequence.Sequence` instances
    
    :param assets: the assets used in this project, it should be a list of
      instances of :class:`~stalker.core.models.asset.Asset`
    
    :param image_format: the output image format of the project, it should be
      an instance of :class:`~stalker.core.models.imageFormat.ImageFormat`
      
    :param fps: the FPS of the project, it should be a float number.
    
    :param type: the type of the project, it should be an instance of
      :class:`~stalker.core.models.types.ProjectType`
    
    :param structure: the structure of the project, it should be an instance of
      :class:`~stalker.core.models.structure.Structure`
    
    :param repository: the repository that the project files are going to be
      stored in, it should be an instance of
      :class:`~stalker.core.models.repository.Reporsitory`
    
    :param is_stereoscopic: a bool value (True or False), showing if the
      project is going to be a stereo 3D project
    
    :param display_width: the width of the display that the output of the
      project is going to be displayed (very unnecessary if you are not using
      stereo 3D setup)
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Project, self).__init__(**kwargs)


