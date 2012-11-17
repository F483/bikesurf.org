# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


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
KIND_CHOICES = [(kind, kind) for kind in KINDS]


GENDER = [
    'NEUTRAL', 
    'FEMALE', 
    'MALE'
]
GENDER_CHOICES = [(gender, gender) for gender in GENDER]


SIZE = [      # Body Hight
    'SMALL',  # 0cm - 145cm
    'MEDIUM', # 145cm - 175cm
    'LARGE'   # 175cm + 
]
SIZE_CHOICES = [(size, size) for size in SIZE]


class Bike(models.Model):

    owner       = models.ForeignKey('auth.User')
    name        = models.CharField(max_length=1024)
    description = models.TextField()
    available   = models.BooleanField(default=True)
    reserve     = models.BooleanField(default=False) # not requestable
    station     = models.ForeignKey('station.Station') # must belong to owner or team member
    lockcode    = models.CharField(max_length=1024)
    keycode     = models.CharField(max_length=1024)
    
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

    def __unicode__(self):
        args = (self.id, self.owner.id, self.name)
        return u"id: %s; owner_id: %s; name: %s" % args


class Picture(models.Model):

    bike        = models.ForeignKey('bike.Bike')
    image       = models.ImageField(upload_to='db/bike_images') # FIXME use hash as name to avoid collisisons
    preview     = models.BooleanField(default=False)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id)
        return u"id: %s; bike_id: %s" % args


class Issue(models.Model):

    bike        = models.ForeignKey('bike.Bike')
    problem     = models.TextField() # by notifier
    solution    = models.TextField() # by reslver
    resolved    = models.BooleanField(default=False)
    notifier    = models.ForeignKey('auth.User', related_name='issues_notified')
    resolver    = models.ForeignKey('auth.User', related_name='issues_resolved')

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id)
        return u"id: %s; bike_id: %s" % args


