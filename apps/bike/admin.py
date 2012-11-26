# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from apps.bike.models import Bike
from apps.bike.models import Issue


admin.site.register(Bike)
admin.site.register(Issue)


