# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.site.views',
    url(r'^$', 'root'), # index or under construction
    url(r'^accounts/profile/$', 'profile'),
)

