# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _


STATES = [
    "REQUEST",   # (B)                       borrow.active: False -> False
    "UNSURE",    # (L)   Require Meetup      borrow.active: False -> True
    "ACCEPTED",  # (L)                       borrow.active: False -> True
    "REJECTED",  # (L)                       borrow.active: False -> False
    "CANCLED",   # (B|L) Only Before Start   borrow.active: True  -> False
    "UNLOCATED", # (L)   Not at Station      borrow.active: True  -> False
    "DAMAGED",   # (L)   Doesnt work ...     borrow.active: True  -> False  bike.active: True -> False
    "MISSING",   # (B|L) Stolen ...          borrow.active: True  -> False  bike.active: True -> False
    "RETURNED",  # (B)   Borrower Rated      borrow.active: True  -> True
    "FINISHED",  # (L)   Lender Rated        borrow.active: True  -> False
]
STATE_CHOICES = [(state, _(state)) for state in STATES]


class Borrow(models.Model):

    bike        = models.ForeignKey('bike.Bike')
    borrower    = models.ForeignKey('account.Account')
    start       = models.DateField()
    finish      = models.DateField() # inclusive
    active      = models.BooleanField()
    state       = models.CharField(max_length=256, choices=STATE_CHOICES)
    
    # location
    src         = models.ForeignKey('station.Station', related_name='borrows_outgoing')
    dest        = models.ForeignKey('station.Station', related_name='borrows_incoming')

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id, self.state, self.start, self.finish)
        return u"id: %s; bike_id: %s; state: %s; start: %s; finish %s" % args


class Log(models.Model):

    borrow      = models.ForeignKey('borrow.Borrow')
    initiator   = models.ForeignKey('account.Account') # None => system
    state       = models.CharField(max_length=256, choices=STATE_CHOICES)
    note        = models.TextField() # by initiator

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.state, self.created_on)
        return u"id: %s; borrow_id: %s; state %s; created_on: %s" % args


class Rating(models.Model): # only borrower rates ...

    borrow      = models.ForeignKey('borrow.Borrow')
    rating      = models.IntegerField() # 0 - 5 'Stars' TODO validate range
    account     = models.ForeignKey('account.Account') # borrower or lender

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.rating)
        return u"id: %s; borrow_id: %s; rating: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('borrow', 'account'),) 

