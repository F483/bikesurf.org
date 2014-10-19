# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import hashlib
import os.path
from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill
from apps.account.models import Account


class Gallery(models.Model):

    team = models.ForeignKey(
        'team.Team', related_name="galleries", null=True, blank=True
    )

    primary = models.ForeignKey(
        'gallery.Picture', related_name="primary", null=True, blank=True
    )

    # metadata
    created_by  = models.ForeignKey(Account, related_name="galleries_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey(Account, related_name="galleries_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.id


def _get_upload_path(prefix, data):
    hasher = hashlib.sha1()
    for chunk in data.chunks():
        hasher.update(chunk)
    digest = hasher.hexdigest()
    return "gallery/%s/%s.%s" % (prefix, digest, 'jpeg')


def _image_upload_to(instance, filename, **kwargs):
    return _get_upload_path("images", instance.image)


def _thumbnail_upload_to(instance, filename, **kwargs):
    return _get_upload_path("thumbnails", instance.thumbnail)


def _preview_upload_to(instance, filename, **kwargs):
    return _get_upload_path("previews", instance.preview)


class Picture(models.Model):

    gallery = models.ForeignKey('gallery.Gallery', related_name="pictures")

    image = ProcessedImageField(
        upload_to=_image_upload_to, 
        processors=[ResizeToFill(640, 480)],
        format='JPEG', options={'quality': 90}
    )

    preview = ProcessedImageField(
        upload_to=_preview_upload_to, 
        processors=[ResizeToFill(320, 240)],
        format='JPEG', options={'quality': 90}
    )

    thumbnail = ProcessedImageField(
        upload_to=_thumbnail_upload_to, 
        processors=[ResizeToFill(100, 75)],
        format='JPEG', options={'quality': 90}
    )

    # metadata
    created_by  = models.ForeignKey(Account, related_name="pictures_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey(Account, related_name="pictures_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.id

