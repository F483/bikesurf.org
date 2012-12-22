# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',

    url(r'^', include('apps.site.urls')),
    url(r'^team/', include('apps.team.urls')),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


