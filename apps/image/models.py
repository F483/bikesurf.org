# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


class Image(models.Model):

    image       = models.ImageField(upload_to='data/images')
    preview     = models.BooleanField(default=False)
    
    # relations 
    user        = models.ForeignKey('auth.User', null=True, blank=True)
    bike        = models.ForeignKey('bike.Bike', null=True, blank=True)
    station     = models.ForeignKey('station.Station', null=True, blank=True)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.preview)
        return u"id: %s; preview: %s" % args


