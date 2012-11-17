# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from bike.models import Bike
from bike.models import Picture
from bike.models import Issue


admin.site.register(Bike)
admin.site.register(Picture)
admin.site.register(Issue)


