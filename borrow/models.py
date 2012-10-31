from django.db import models
from django.contrib.auth.models import User
from bike.models import Bike


class Borrow(models.Model):

    borrower    = models.ForeignKey(User)
    start       = models.DateField()
    finish      = models.DateField() # inclusive
    state       = models.CharField(max_length=256) # 'request', 'accepted', 'confirmed', 'cancled', 'stolen', etc ...
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()


class BorrowLog(models.Model):

    borrow      = models.ForeignKey(Borrow)
    initiator   = models.ForeignKey(User) # None => system
    state       = models.CharField(max_length=256) # 'request', 'accepted', 'confirmed', 'cancled', 'stolen', etc ...
    
    # meta
    created_on  = models.DateTimeField()


class BorrowRating(models.Model): # only borrower rates ...

    borrow      = models.ForeignKey(Borrow)
    rating      = models.IntegerField() # 0 - 5 'Stars'

    # meta
    created_on  = models.DateTimeField()
