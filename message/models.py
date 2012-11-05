from django.db import models
from django.contrib.auth.models import User
from bike.models import Bike
from borrow.models import Borrow


class Message(models.Model):

    sender      = models.ForeignKey(User, related_name='messages_sent') # None => system
    recipient   = models.ForeignKey(User, related_name='messages_received')
    content     = models.TextField()
   
    # related
    bike        = models.ForeignKey(Bike)
    borrow      = models.ForeignKey(Borrow)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.sender.id, self.recipient.id)
        return u"id: %s; sender_id: %s; recipient_id: %s" % args
