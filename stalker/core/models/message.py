#-*- coding: utf-8 -*-




from stalker.core.models import entity, mixin





########################################################################
class Message(entity.Entity, mixin.StatusMixin):
    """The base of the messaging system in Stalker
    
    Messages are one of the ways to collaborate in Stalker. The model of the
    messages is taken from the e-mail system. So it is pretty similiar to an
    e-mail message.
    
    :param from: the :class:`~stalker.core.models.user.User` object sending the
      message
    
    :param to: the list of :class:`~stalker.core.models.user.User`\ s to
      receive this message
    
    :param subject: the subject of the message
    
    :param body: the body of the message
    
    :param in_reply_to: the :class:`~stalker.core.models.message.Message`
      object which this message is a reply to.
    
    :param replies: the list of :class:`~stalker.core.models.message.Message`
      objects which are the direct replies of this message
    
    :param attachments: a list of
      :class:`~stalker.core.models.entity.SimpleEntity` objects attached to
      this message (so anything can be attached to a message)
    
    """
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)