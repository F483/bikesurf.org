# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField


class Station(models.Model):

    team        = models.ForeignKey("team.Team", related_name="stations")
    responsable = models.ForeignKey("account.Account")
    capacity    = models.IntegerField(default=1)
    active      = models.BooleanField(default=True)
    street      = models.CharField(max_length=1024)
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = CountryField()
    # TODO link on google maps 
    # TODO image galerie
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (
            self.country.name, 
            self.postalcode, 
            self.city, 
            self.street, 
            self.responsable
        )
        return u"%s - %s %s - %s (%s)" % args



