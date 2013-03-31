# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from apps.gallery.models import Gallery
from apps.gallery.models import Picture
from apps.team.utils import assert_member


# XXX http://www.fontsquirrel.com/fonts/League-Gothic

def setprimary(account, picture, gallery):
    if ((gallery.team and account not in gallery.team.members.all()) or 
            (not gallery.team and gallery.created_by != account)):
        raise PermissionDenied
    if picture not in gallery.pictures.all():
        raise Exception("Cannot set primary picture to non gallery picture!")
    gallery.primary = picture
    gallery.save()


def add(account, image, gallery):
    if ((gallery.team and account not in gallery.team.members.all()) or 
            (not gallery.team and gallery.created_by != account)):
        raise PermissionDenied
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


