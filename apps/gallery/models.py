# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import hashlib
import os.path
from django.db import models


class Gallery(models.Model):

    primary      = models.ForeignKey('gallery.Picture', related_name="primary", null=True, blank=True)

    # TODO put meta in parent class
    #created_by  = models.ForeignKey('account.Account', null=True, blank=True)
    #created_on  = models.DateTimeField(auto_now_add=True)

    #def __unicode__(self):
    #    return u"id: %s" % self.id


def _get_upload_path(prefix, data, filename):
    hasher = hashlib.sha1()
    for chunk in data.chunks():
        hasher.update(chunk)
    digest = hasher.hexdigest()
    base, ext = os.path.splitext(filename)
    # TODO TEST UNTRUSTED USER FILES AND FILENAMES!!!!!!!
    return "%s/%s%s" % (prefix.lower(), digest.lower(), ext.lower())


def _image_upload_to(instance, filename, **kwargs):
    return _get_upload_path("images", instance.image_data, filename)


def _thumbnail_upload_to(instance, filename, **kwargs):
    return _get_upload_path("thumbnails", instance.thumbnail_data, filename)


class Picture(models.Model):

    gallery = models.ForeignKey('gallery.Gallery', related_name="pictures")

    image_data = models.ImageField(
            upload_to=_image_upload_to, max_length=255, 
            height_field='image_height', width_field='image_width'
    )
    image_height     = models.PositiveIntegerField(default=0, editable=False)
    image_width      = models.PositiveIntegerField(default=0, editable=False)

    thumbnail_data = models.ImageField(
            upload_to=_thumbnail_upload_to, max_length=255, 
            height_field='image_height', width_field='image_width'
    )
    thumbnail_height = models.PositiveIntegerField(default=0, editable=False)
    thumbnail_width = models.PositiveIntegerField(default=0, editable=False)

    # TODO put meta in parent class
    #created_by  = models.ForeignKey('account.Account', null=True, blank=True)
    #created_on  = models.DateTimeField(auto_now_add=True)

    #def __unicode__(self):
    #    return u"id: %s" % self.id


