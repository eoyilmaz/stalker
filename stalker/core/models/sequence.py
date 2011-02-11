#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin






########################################################################
class Sequence(entity.Entity, mixin.ReferenceMixin, mixin.StatusMixin):
    """Stores data about Sequences.
    
    
    A Sequence is a holder of :class:`~stalker.core.models.shot.Shot` objects.
    
    :param project: The :class:`~stalker.core.models.project.Project` that this
      Sequence belongs to.
    
    :param shots: The list of :class:`~stalker.core.models.shot.Shot` objects
      that this Sequence has.
    
    :param lead: The lead of this Seuqence, it is a
      :class:`~stalker.core.models.user.User` instance.
    
    :param start_date: The :class:`datetime.datetime` instance showing the
      start date.
    
    :param due_date: The :class:`
    """
    
    
    
    pass
