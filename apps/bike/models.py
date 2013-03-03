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


SIZE_CHOICES = [      # Body Hight
    ('SMALL', _('SMALL')),  # 0cm - 145cm
    ('MEDIUM', _('MEDIUM')), # 145cm - 175cm
    ('LARGE', _('LARGE'))   # 175cm + 
]


class Bike(Model):

    # main data
    team = ForeignKey('team.Team', related_name='bikes')
    name = CharField(max_length=1024)
    description = TextField()
    active = BooleanField(default=True)
    reserve = BooleanField(default=False) # not requestable
    station = ForeignKey('station.Station', blank=True, null=True, related_name="bikes")
    lockcode = CharField(max_length=1024)
    size = CharField(max_length=64, choices=SIZE_CHOICES, default='MEDIUM') # TODO add height in cm
    lights = BooleanField(default=False) # to cycle when dark
    
    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    # TODO validation
    # TODO galerie

    def __unicode__(self):
        return self.name


