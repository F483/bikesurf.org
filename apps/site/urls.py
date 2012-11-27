# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'apps.site.views.root'), # index and dashboard
)

