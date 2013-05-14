# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.account.views',
    url(r'^accounts/profile/$',     'view'), # use this url because of allauth
    url(r'^account/edit$',          'edit'),
)

