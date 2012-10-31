from django.db import models
from django.contrib.auth.models import User
from bike.models import Bike
from borrow.models import Borrow


class Message(models.Model):

    sender      = models.ForeignKey(User, related_name='sent_messages')
    recipient   = models.ForeignKey(User, related_name='received_messages')
    content     = models.TextField()
   
    # related
    bike        = models.ForeignKey(Bike)
    borrow      = models.ForeignKey(Borrow)

    # meta
    created_on  = models.DateTimeField()

