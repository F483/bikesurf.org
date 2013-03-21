# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from apps.gallery.models import Picture
from apps.gallery.models import Gallery
from django.contrib import admin

admin.site.register(Picture)
admin.site.register(Gallery)
