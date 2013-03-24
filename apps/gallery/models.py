# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import hashlib
import os.path
from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


class Gallery(models.Model):

    team = models.ForeignKey(
        'team.Team', related_name="galleries", null=True, blank=True
    )

    primary = models.ForeignKey(
        'gallery.Picture', related_name="primary", null=True, blank=True
    )

    # metadata
    created_by  = models.ForeignKey('account.Account', related_name="galleries_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey("account.Account", related_name="galleries_updated")
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
    return _get_upload_path("images", instance.image_data)


def _thumbnail_upload_to(instance, filename, **kwargs):
    return _get_upload_path("thumbnails", instance.thumbnail_data)


def _preview_upload_to(instance, filename, **kwargs):
    return _get_upload_path("previews", instance.preview_data)


class Picture(models.Model):

    gallery = models.ForeignKey('gallery.Gallery', related_name="pictures")

    # image fields
    image_height = models.PositiveIntegerField(default=0, editable=False)
    image_width = models.PositiveIntegerField(default=0, editable=False)
    image_data = ProcessedImageField(
        upload_to=_image_upload_to, 
        height_field='image_height', width_field='image_width',
        processors=[ResizeToFill(640, 480)],
        format='JPEG', options={'quality': 90}
    )

    # preview fields
    preview_height = models.PositiveIntegerField(default=0, editable=False)
    preview_width = models.PositiveIntegerField(default=0, editable=False)
    preview_data = ProcessedImageField(
        upload_to=_preview_upload_to, 
        height_field='preview_height', width_field='preview_width',
        processors=[ResizeToFill(320, 240)],
        format='JPEG', options={'quality': 90}
    )

    # thumbnail fields
    thumbnail_height = models.PositiveIntegerField(default=0, editable=False)
    thumbnail_width = models.PositiveIntegerField(default=0, editable=False)
    thumbnail_data = ProcessedImageField(
        upload_to=_thumbnail_upload_to, 
        height_field='thumbnail_height', width_field='thumbnail_width',
        processors=[ResizeToFill(100, 75)],
        format='JPEG', options={'quality': 90}
    )

    # metadata
    created_by  = models.ForeignKey('account.Account', related_name="pictures_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey("account.Account", related_name="pictures_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.id

