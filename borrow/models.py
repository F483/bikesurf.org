from django.db import models
from django.contrib.auth.models import User
from bike.models import Bike


STATES = [
    'REQUEST', 
    'ACCEPTED', 
#    'COMFIRMED', # might be needed
    'CANCLED', 
    'DAMAGED', 
    'MISSING',
    'RETURNED',
]
STATE_CHOICES = [(state, state) for state in STATES]


class Borrow(models.Model):

    bike        = models.ForeignKey(Bike)
    borrower    = models.ForeignKey(User)
    start       = models.DateField()
    finish      = models.DateField() # inclusive
    state       = models.CharField(max_length=256, choices=STATE_CHOICES)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id, self.state, self.start, self.finish)
        return u"id: %s; bike_id: %s; state: %s; start: %s; finish %s" % args


class BorrowLog(models.Model):

    borrow      = models.ForeignKey(Borrow)
    initiator   = models.ForeignKey(User) # borrower or bike owner. None => system
    state       = models.CharField(max_length=256, choices=STATE_CHOICES)
    note        = models.TextField()
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.state, self.created_on)
        return u"id: %s; borrow_id: %s; state %s; created_on: %s" % args


class BorrowRating(models.Model): # only borrower rates ...

    borrow      = models.ForeignKey(Borrow)
    rating      = models.IntegerField() # 0 - 5 'Stars' TODO validate range

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.rating)
        return u"id: %s; borrow_id: %s; rating: %s" % args


