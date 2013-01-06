# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
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


class Bike(models.Model):

    # main data
    owner       = models.ForeignKey('account.Account', related_name='bikes')
    team        = models.ForeignKey('team.Team', related_name='bikes')
    name        = models.CharField(max_length=1024)
    description = models.TextField()
    active      = models.BooleanField(default=True)
    reserve     = models.BooleanField(default=False) # not requestable
    station     = models.ForeignKey('station.Station', blank=True, null=True)
    lockcode    = models.CharField(max_length=1024)
    keycode     = models.CharField(max_length=1024, blank=True)
    
    # Usefull properties to filter by.
    kind        = models.CharField(max_length=256, choices=KIND_CHOICES, default='NORMAL')
    gender      = models.CharField(max_length=256, choices=GENDER_CHOICES, default='NEUTRAL')
    size        = models.CharField(max_length=256, choices=SIZE_CHOICES, default='MEDIUM')
    lights      = models.BooleanField(default=False) # to cycle when dark
    fenders     = models.BooleanField(default=False) # to cycle when wet
    rack        = models.BooleanField(default=False) # to carry stuff
    basket      = models.BooleanField(default=False) # to put stuff in
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation
    # TODO galerie

    def __unicode__(self):
        return self.name


class Issue(models.Model):

    bike        = models.ForeignKey('bike.Bike')
    problem     = models.TextField() # by notifier
    solution    = models.TextField() # by reslver
    resolved    = models.BooleanField(default=False)
    notifier    = models.ForeignKey('account.Account', related_name='issues_notified')
    resolver    = models.ForeignKey('account.Account', related_name='issues_resolved')

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id)
        return u"id: %s; bike_id: %s" % args


