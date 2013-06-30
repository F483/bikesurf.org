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
    gallery = ForeignKey('gallery.Gallery')
    description = TextField()
    active = BooleanField(default=True)
    reserve = BooleanField(default=False) # not requestable
    station = ForeignKey('station.Station', related_name="bikes")
    lockcode = CharField(max_length=1024)
    size = CharField(max_length=64, choices=SIZE_CHOICES, default='MEDIUM')
    lights = BooleanField(default=False) # to cycle when dark
    
    # metadata
    created_by  = ForeignKey('account.Account', related_name="bikes_created")
    created_on  = DateTimeField(auto_now_add=True)
    updated_by  = ForeignKey("account.Account", related_name="bikes_updated")
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


