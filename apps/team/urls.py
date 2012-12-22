# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from common.shortcuts import URL_NAME


urlpatterns = patterns('',
    url(r'^(?P<team_name>%s)$' % URL_NAME, 'apps.team.views.blog'),
    url(r'^(?P<team_name>%s)/blog$' % URL_NAME, 'apps.team.views.blog'),
    url(r'^(?P<team_name>%s)/bikes$' % URL_NAME, 'apps.team.views.bikes'),
    url(r'^(?P<team_name>%s)/members$' % URL_NAME, 'apps.team.views.members'),
    url(r'^(?P<team_name>%s)/(?P<page_name>%s)$' % (URL_NAME, URL_NAME), 'apps.team.views.page'),
)


