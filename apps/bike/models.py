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


KINDS = [
    'NORMAL', # comfort, hybrid, trekking, citybike
    'BMX', 
    'CARGOBIKE',
    'CRUISER',
    'ELECTRIC', 
    'FIXIE', 
    'FOLDING', 
    'KIDS',
    'MOUNTAINBIKE', 
    'RECUMBENT',
    'ROADBIKE', 
    'TANDEM',
    'TRICYCLE',
    'UNICYCLE',
]
KIND_CHOICES = [(kind, _(kind)) for kind in KINDS]


GENDER = [
    'NEUTRAL', 
    'FEMALE', 
    'MALE'
]
GENDER_CHOICES = [(gender, _(gender)) for gender in GENDER]


SIZE = [      # Body Hight
    'SMALL',  # 0cm - 145cm
    'MEDIUM', # 145cm - 175cm
    'LARGE'   # 175cm + 
]
SIZE_CHOICES = [(size, _(size)) for size in SIZE]


class Bike(Model):

    # main data
    owner = ForeignKey('account.Account', related_name='bikes')
    team = ForeignKey('team.Team', related_name='bikes')
    name = CharField(max_length=1024)
    description = TextField()
    active = BooleanField(default=True)
    reserve = BooleanField(default=False) # not requestable
    station = ForeignKey('station.Station', blank=True, null=True)
    lockcode = CharField(max_length=1024)
    keycode = CharField(max_length=1024, blank=True)
    
    # Usefull properties to filter by.
    kind = CharField(max_length=64, choices=KIND_CHOICES, default='NORMAL')
    gender = CharField(max_length=64, choices=GENDER_CHOICES, default='NEUTRAL')
    size = CharField(max_length=64, choices=SIZE_CHOICES, default='MEDIUM')
    lights = BooleanField(default=False) # to cycle when dark
    fenders = BooleanField(default=False) # to cycle when wet
    rack = BooleanField(default=False) # to carry stuff
    basket = BooleanField(default=False) # to put stuff in
    
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


