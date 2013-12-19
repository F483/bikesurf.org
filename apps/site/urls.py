# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.site.views',
    url(r'^$', 'index'),
    url(r'^site/terms_and_conditions.html$', 'index'), # TODO generic view
)

