# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from apps.borrow.models import Borrow
from apps.borrow.models import Log
from apps.borrow.models import Rating


admin.site.register(Borrow)
admin.site.register(Log)
admin.site.register(Rating)


