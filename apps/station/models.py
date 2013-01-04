# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField


class Station(models.Model):

    owner       = models.ForeignKey("account.Account")
    preview     = models.ForeignKey("image.Image", related_name="station_previews", blank=True, null=True)
    capacity    = models.IntegerField(default=1)
    active      = models.BooleanField(default=True)
    street      = models.CharField(max_length=1024)
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = CountryField()
    # TODO link on google maps 
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.country.name, self.postalcode, self.city, self.street)
        return u"%s - %s %s - %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (("owner", "street", "city", "postalcode", "country"),) 


