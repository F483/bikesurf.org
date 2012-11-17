# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


STATES = [
    'REQUEST', 
    'UNSURE', # requires meetup
    'ACCEPTED', 
    'CANCLED', 
    'DAMAGED', 
    'MISSING',
    'RETURNED',
]
STATE_CHOICES = [(state, state) for state in STATES]


class Borrow(models.Model):

    bike        = models.ForeignKey('bike.Bike')
    borrower    = models.ForeignKey('auth.User')
    start       = models.DateField()
    finish      = models.DateField() # inclusive
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
    initiator   = models.ForeignKey('auth.User') # None => system
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
    user        = models.ForeignKey('auth.User') # borrower or lender

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.rating)
        return u"id: %s; borrow_id: %s; rating: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('borrow', 'user'),) 

