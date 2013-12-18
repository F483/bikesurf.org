# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import IntegerField
from apps.common.shortcuts import get_object_or_none


STATE_CHOICES = [
    ("REQUEST",_("REQUEST")),    # (B)                        
    ("MEETUP",_("MEETUP")),      # (L)    
    ("ACCEPTED",_("ACCEPTED")),  # (L)    
    ("REJECTED",_("REJECTED")),  # (L)    
    ("CANCELED",_("CANCELED")),  # (B|L)  Only Before Start   
    ("FINISHED",_("FINISHED")),  # (B|L)  Both Rated
]


class Borrow(Model):

    bike = ForeignKey( # None => Bike deleted
            'bike.Bike', related_name="borrows", 
            blank=True, null=True
    )
    team = ForeignKey('team.Team', related_name='borrows') # only because bikes may be deleted
    borrower = ForeignKey('account.Account')
    start = DateField()
    finish = DateField() # inclusive
    active = BooleanField() # if the borrow blocks a timeslot
    state = CharField(max_length=64, choices=STATE_CHOICES)
    src = ForeignKey('station.Station', related_name='departures',
                     blank=True, null=True)
    dest = ForeignKey('station.Station', related_name='arrivals',
                      blank=True, null=True)

    @property
    def borrower_rating(self):
        if self._borrower_rating:
            return self._borrower_rating
        self._borrower_rating = get_object_or_none(
            Rating, borrow=self, originator="BORROWER"
        )
        return self._borrower_rating

    @property
    def lender_rating(self):
        if self._lender_rating:
            return self._lender_rating
        self._lender_rating = get_object_or_none(
            Rating, borrow=self, originator="LENDER"
        )
        return self._lender_rating

    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    def __unicode__(self):
        bike_id = self.bike and self.bike.id or None
        args = (self.id, bike_id, self.state, self.start, self.finish)
        return u"id: %s; bike_id: %s; state: %s; start: %s; finish %s" % args

    class Meta:
        
        ordering = ["start"]


class Log(Model):

    ACTION_CHOICES = [
        ("LENDER_RATE",_("LENDER_RATE")),
        ("BORROWER_RATE",_("BORROWER_RATE")),
        ("CREATE",_("CREATE")),
        ("RESPOND",_("RESPOND")),
        ("CANCEL",_("CANCEL")),
        ("FINISHED",_("FINISHED")),
        ("EDIT", _("EDIT")),
    ]

    borrow = ForeignKey('borrow.Borrow', related_name="logs")
    initiator = ForeignKey('account.Account', blank=True, null=True) # None => system
    action = CharField(max_length=64, choices=ACTION_CHOICES)
    note = TextField(blank=True) # by initiator

    # meta
    # created_by = initiator
    # never updated
    created_on  = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s %s %s" % (self.initiator, self.action, self.borrow.id)

    class Meta:
        
        ordering = ["-created_on"]


ORIGINATOR_CHOICES = [
    ("BORROWER",_("BORROWER")),
    ("LENDER",_("LENDER")),
]


RATING_CHOICES = [
    ("THUMBS_UP", _("THUMBS_UP")),
    ("NEUTRAL", _("NEUTRAL")),
    ("THUMBS_DOWN", _("THUMBS_DOWN")),
]


class Rating(Model):

    borrow = ForeignKey('borrow.Borrow')
    rating = CharField(max_length=64, choices=RATING_CHOICES)
    account = ForeignKey('account.Account') # borrower or lender
    originator = CharField(max_length=64, choices=ORIGINATOR_CHOICES)

    # meta
    created_on  = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        args = (self.id, self.borrow.id, self.rating)
        return u"id: %s; borrow_id: %s; rating: %s" % args

    class Meta:
        
        unique_together = (("borrow", "account", "originator"),) 

