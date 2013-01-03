# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.contrib import admin
from apps.team.models import Team
from apps.team.models import Page
from apps.team.models import Station
from apps.team.models import JoinRequest
from apps.team.models import RemoveRequest


admin.site.register(Team)
admin.site.register(Page)
admin.site.register(Station)
admin.site.register(JoinRequest)
admin.site.register(RemoveRequest)


