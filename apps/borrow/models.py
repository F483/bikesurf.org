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


STATE_CHOICES = [
    ("REQUEST",_("REQUEST")),    # (B)                        
    ("MEETUP",_("MEETUP")),      # (L)    
    ("ACCEPTED",_("ACCEPTED")),  # (L)    
    ("REJECTED",_("REJECTED")),  # (L)    
    ("CANCELED",_("CANCELED")),  # (B|L)  Only Before Start   
    ("FINISHED",_("FINISHED")),  # (B|L)  Both Rated
]


class Borrow(Model):

    bike = ForeignKey('bike.Bike', related_name="borrows")
    borrower = ForeignKey('account.Account')
    start = DateField()
    finish = DateField() # inclusive
    active = BooleanField() # if the borrow blocks a timeslot
    state = CharField(max_length=64, choices=STATE_CHOICES)
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

    ACTION_CHOICES = [
        ("RATE_TEAM",_("RATE_TEAM")),
        ("RATE_MY",_("RATE_MY")),
        ("CREATE",_("CREATE")),
        ("RESPOND",_("RESPOND")),
        ("CANCEL",_("CANCEL")),
        ("FINISHED",_("FINISHED")),
    ]

    borrow = ForeignKey('borrow.Borrow', related_name="logs")
    initiator = ForeignKey('account.Account', blank=True, null=True) # None => system
    action = CharField(max_length=64, choices=ACTION_CHOICES)
    note = TextField(blank=True) # by initiator

    # meta
    created_on  = DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        return u"%s %s %s" % (self.initiator, self.action, self.borrow.id)

    class Meta:
        
        ordering = ["-created_on"]


class Rating(Model): # only borrower rates ...

    ORIGINATOR_CHOICES = [
        ("BORROWER",_("BORROWER")),
        ("LENDER",_("LENDER")),
    ]

    borrow = ForeignKey('borrow.Borrow')
    rating = IntegerField() # 0 - 5 'Stars'
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

