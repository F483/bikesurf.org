# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.core.exceptions import PermissionDenied
from apps.gallery.models import Gallery
from apps.gallery.models import Picture
from apps.team.utils import assert_member
from apps.team import control as team_control


def can_edit(account, gallery):
    return not ((gallery.team and not team_control.is_member(account, gallery.team)) or 
                (not gallery.team and gallery.created_by != account))


def _assert_can_edit(account, gallery):
    if not can_edit(account, gallery):
        raise PermissionDenied


def delete(account, gallery):
    """ Delete gallery and all pictures belonging to it. """
    _assert_can_edit(account, gallery)
    for picture in gallery.pictures.all():
        remove(account, picture)
    gallery.delete()


def remove(account, picture):
    """ Remove picture from the gallery and delete the image file on server. """
    gallery = picture.gallery
    _assert_can_edit(account, gallery)
    if gallery.primary == picture:
        gallery.primary = None
        gallery.updated_by = account
        gallery.save()
    os.remove(picture.image.path)
    os.remove(picture.preview.path)
    os.remove(picture.thumbnail.path)
    picture.delete()
    return gallery


def setprimary(account, picture):
    """ Set picture as the galleries primary picture. """
    gallery = picture.gallery
    _assert_can_edit(account, gallery)
    gallery.primary = picture
    gallery.save()


def add(account, image, gallery):
    """ Add a picture to the gallery. """
    _assert_can_edit(account, gallery)
    picture = Picture()
    picture.image = image
    picture.preview = image
    picture.thumbnail = image
    picture.gallery = gallery
    picture.created_by = account
    picture.updated_by = account
    picture.save()
    return picture


def create(account, image, team):
    """ Create a new gallery. """
    if team:
        assert_member(account, team)
    gallery = Gallery()
    gallery.created_by = account
    gallery.updated_by = account
    gallery.team = team
    gallery.save()
    picture = add(account, image, gallery)
    gallery.primary = picture
    gallery.save()
    return gallery


