# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from apps.gallery.models import Gallery
from apps.gallery.models import Picture
from apps.team.utils import assert_member


# XXX http://www.fontsquirrel.com/fonts/League-Gothic


def create(account, image, team):
    if team:
        assert_member(account, team)
    gallery = Gallery()
    gallery.created_by = account
    gallery.updated_by = account
    gallery.team = team
    gallery.save()
    picture = Picture()
    picture.image_data = image
    picture.preview_data = image
    picture.thumbnail_data = image
    picture.gallery = gallery
    picture.created_by = account
    picture.updated_by = account
    picture.save()
    gallery.primary = picture
    gallery.save()
    return gallery


