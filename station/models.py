# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


class Station(models.Model):

    owner       = models.ForeignKey('auth.User')
    capacity    = models.IntegerField(default=1)
    street      = models.CharField(max_length=1024)
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = models.CharField(max_length=1024) # TODO make enum choices
    # TODO link on google maps 
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.owner.id, self.street, self.postalcode, self.city, self.country)
        return u"id: %s; owner_id: %s; %s, %s, %s, %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('owner', 'street', 'city', 'postalcode', 'country'),) 
