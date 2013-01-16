# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import IntegerField


STATES = [
    "REQUEST",   # (B)                        
    "MEETUP",    # (L)    
    "ACCEPTED",  # (L)    
    "REJECTED",  # (L)    
    "CANCELED",  # (B|L)  Only Before Start   
    "FINISHED",  # (B|L)  Both Rated
]
STATE_CHOICES = [(state, _(state)) for state in STATES]


class Borrow(Model):

    bike = ForeignKey('bike.Bike')
    borrower = ForeignKey('account.Account')
    start = DateField()
    finish = DateField() # inclusive
    active = BooleanField() # if the borrow blocks a timeslot
    state = CharField(max_length=256, choices=STATE_CHOICES)
    src = ForeignKey('station.Station', related_name='borrows_outgoing')
    dest = ForeignKey('station.Station', related_name='borrows_incoming')

    # meta
    created_on  = DateTimeField(auto_now_add=True)
    updated_on  = DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id, self.state, self.start, self.finish)
        return u"id: %s; bike_id: %s; state: %s; start: %s; finish %s" % args


class Log(Model):

    ACTIONS = [
        "RATE_TEAM",
        "RATE_MY",
        "CREATE",
        "RESPOND",
        "CANCEL",
        "FINISHED",
    ]
    ACTION_CHOICES = [(action, _(action)) for action in ACTIONS]

    borrow = ForeignKey('borrow.Borrow', related_name="logs")
    initiator = ForeignKey('account.Account', blank=True, null=True) # None => system
    action = CharField(max_length=64, choices=ACTION_CHOICES)
    note = TextField(blank=True) # by initiator

    # meta
    created_on  = DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.state, self.created_on)
        return u"id: %s; borrow_id: %s; state %s; created_on: %s" % args


class Rating(Model): # only borrower rates ...

    ORIGINATOR = [
        "BORROWER",
        "LENDER",
    ]
    ORIGINATOR_CHOICES = [(o, _(o)) for o in ORIGINATOR]

    borrow = ForeignKey('borrow.Borrow')
    rating = IntegerField() # 0 - 5 'Stars' TODO validate range
    account = ForeignKey('account.Account') # borrower or lender
    originator = CharField(max_length=64, choices=ORIGINATOR_CHOICES)

    # meta
    created_on  = DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.rating)
        return u"id: %s; borrow_id: %s; rating: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (("borrow", "account", "originator"),) 

