# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateTimeField
from django.utils.translation import ugettext_lazy as _


KIND_CHOICES = [
    ('NORMAL', _('NORMAL')), # comfort, hybrid, trekking, citybike
    ('BMX', _('BMX')), 
    ('CARGOBIKE', _('CARGOBIKE')),
    ('CRUISER', _('CRUISER')),
    ('ELECTRIC', _('ELECTRIC')), 
    ('FIXIE', _('FIXIE')), 
    ('FOLDING', _('FOLDING')), 
    ('KIDS', _('KIDS')),
    ('MOUNTAINBIKE', _('MOUNTAINBIKE')), 
    ('RECUMBENT', _('RECUMBENT')),
    ('ROADBIKE', _('ROADBIKE')), 
    ('TANDEM', _('TANDEM')),
    ('TRICYCLE', _('TRICYCLE')),
    ('UNICYCLE', _('UNICYCLE')),
]


GENDER_CHOICES = [
    ('NEUTRAL', _('NEUTRAL')), 
    ('FEMALE', _('FEMALE')), 
    ('MALE', _('MALE'))
]


SIZE_CHOICES = [      # Body Hight
    ('SMALL', _('SMALL')),  # 0cm - 145cm
    ('MEDIUM', _('MEDIUM')), # 145cm - 175cm
    ('LARGE', _('LARGE'))   # 175cm + 
]


class Bike(Model):

    # main data
    owner = ForeignKey('account.Account', related_name='bikes')
    team = ForeignKey('team.Team', related_name='bikes')
    name = CharField(max_length=1024)
    description = TextField()
    active = BooleanField(default=True)
    reserve = BooleanField(default=False) # not requestable
    station = ForeignKey('station.Station', blank=True, null=True, related_name="bikes")
    lockcode = CharField(max_length=1024)
    keycode = CharField(max_length=1024, blank=True) # TODO remove
    
    # Usefull properties to filter by.
    kind = CharField(max_length=64, choices=KIND_CHOICES, default='NORMAL') # TODO remove
    gender = CharField(max_length=64, choices=GENDER_CHOICES, default='NEUTRAL') # TODO remove
    size = CharField(max_length=64, choices=SIZE_CHOICES, default='MEDIUM') # TODO add height in cm
    lights = BooleanField(default=False) # to cycle when dark
    fenders = BooleanField(default=False) # TODO remove
    rack = BooleanField(default=False) # TODO remove
    basket = BooleanField(default=False) # TODO remove
    
    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    # TODO validation
    # TODO galerie

    def __unicode__(self):
        return self.name


class Issue(Model):

    bike = ForeignKey('bike.Bike')
    problem = TextField() # by notifier
    solution = TextField() # by reslver
    resolved = BooleanField(default=False)
    notifier = ForeignKey('account.Account', related_name='issues_notified')
    resolver = ForeignKey('account.Account', related_name='issues_resolved')

    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id)
        return u"id: %s; bike_id: %s" % args


