# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF


urlpatterns = patterns('',
    url(r'^t/create$', 'apps.team.views.create'),
    url(r'^(?P<team_link>%s)$' % HLF, 'apps.team.views.blog'),
    url(r'^(?P<team_link>%s)/$' % HLF, 'apps.team.views.blog'),
    url(r'^(?P<team_link>%s)/blog$' % HLF, 'apps.team.views.blog'),
    url(r'^(?P<team_link>%s)/bikes$' % HLF, 'apps.team.views.bikes'),
    url(r'^(?P<team_link>%s)/borrows$' % HLF, 'apps.team.views.borrows'),
    url(r'^(?P<team_link>%s)/stations$' % HLF, 'apps.team.views.stations'),
    url(r'^(?P<team_link>%s)/members$' % HLF, 'apps.team.views.members'),

    url(r'^(?P<team_link>%s)/join_request$' % HLF, 'apps.team.views.join_request'),
    url(r'^(?P<team_link>%s)/join_requested$' % HLF, 'apps.team.views.join_requested'),
    url(r'^(?P<team_link>%s)/join_requests$' % HLF, 'apps.team.views.join_requests'),

    url(r'^(?P<team_link>%s)/remove_requests$' % HLF, 'apps.team.views.remove_requests'),
    url(r'^(?P<team_link>%s)/(?P<page_link>%s)$' % (HLF, HLF), 'apps.team.views.page'),
)


