# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Image(models.Model):

    photo       = ThumbnailerImageField(upload_to='images', blank=True)
    
    # meta
    created_by  = models.ForeignKey('account.Account', null=True, blank=True)
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        return u"id: %s" % self.id


