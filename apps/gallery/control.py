# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from apps.gallery.models import Gallery
from apps.gallery.models import Picture

# XXX check out https://github.com/mirumee/django-images/blob/master/django_images/models.py
# XXX http://www.fontsquirrel.com/fonts/League-Gothic


def create(account, image):
    # TODO add account and meta data
    gallery = Gallery()
    gallery.save()
    picture = Picture()
    picture.image_data = image
    picture.thumbnail_data = image
    picture.gallery = gallery
    picture.save()
    gallery.primary = picture
    gallery.save()
    return gallery


