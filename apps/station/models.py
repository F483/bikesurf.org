# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.utils.translation import ugettext as _
from django_countries import CountryField


class Station(Model):

    team        = ForeignKey("team.Team", related_name="stations")
    responsible = ForeignKey("account.Account")
    active      = BooleanField(default=True)
    street      = CharField(max_length=1024)
    city        = CharField(max_length=1024)
    postalcode  = CharField(max_length=1024)
    
    # metadata
    created_by  = ForeignKey('account.Account', related_name="stations_created")
    created_on  = DateTimeField(auto_now_add=True)
    updated_by  = ForeignKey("account.Account", related_name="stations_updated")
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (
            self.postalcode, 
            self.city, 
            self.street, 
            self.responsible
        )
        return u"%s %s / %s (%s)" % args


