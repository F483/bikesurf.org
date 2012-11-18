# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from cyclist.models import Cyclist
from cyclist.models import Profile
from cyclist.models import Member


admin.site.register(Cyclist)
admin.site.register(Profile)
admin.site.register(Member)


