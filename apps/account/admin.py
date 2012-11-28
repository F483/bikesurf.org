# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from apps.account.models import Account
from apps.account.models import Site
from apps.account.models import Vacation
from apps.account.models import JoinRequest
from apps.account.models import RemoveRequest


admin.site.register(Account)
admin.site.register(Site)
admin.site.register(Vacation)
admin.site.register(JoinRequest)
admin.site.register(RemoveRequest)


