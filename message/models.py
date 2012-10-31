from django.db import models
from django.contrib.auth.models import User
from bike.models import Bike
from borrow.models import Borrow


class Message(models.Model):

    sender      = models.ForeignKey(User, related_name='messages_sent')
    recipient   = models.ForeignKey(User, related_name='messages_received')
    content     = models.TextField()
   
    # related
    bike        = models.ForeignKey(Bike)
    borrow      = models.ForeignKey(Borrow)

    # meta
    created_on  = models.DateTimeField()

