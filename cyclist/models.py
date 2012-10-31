from django.db import models
from django.contrib.auth.models import User
from address.models import Address


class Cyclist(models.Model):

    user        = models.ForeignKey(User)
    description = models.TextField()
    is_group    = models.BooleanField(default=False)
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()


class CyclistMember(models.Model):

    member      = models.ForeignKey(Cyclist)
    group       = models.ForeignKey(Cyclist)
    role        = models.CharField(max_length=256)   # 'admin', 'mechanic', etc ...

    # meta
    created_on  = models.DateTimeField()
