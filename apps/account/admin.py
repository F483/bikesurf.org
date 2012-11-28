# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from apps.account.models import Account
from apps.account.models import Site
from apps.account.models import Vacation


admin.site.register(Account)
admin.site.register(Site)
admin.site.register(Vacation)


