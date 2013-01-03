# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF


T = "(?P<team_link>%s)" % HLF # Team Link
P = "(?P<page_link>%s)" % HLF # Page Link
JR = "(?P<join_request_id>[0-9]+)" # Join Request Link


urlpatterns = patterns('apps.team.views',

    url(r'^t/create$',                              'create'),

    url(r'^%s/bikes$' % T,                          'bikes'),
    url(r'^%s/borrows$' % T,                        'borrows'),
    url(r'^%s/stations$' % T,                       'stations'),
    url(r'^%s/members$' % T,                        'members'),

    url(r'^%s/join_request$' % T,                   'join_request'),
    url(r'^%s/join_requested$' % T,                 'join_requested'),
    url(r'^%s/join_requests$' % T,                  'join_requests'),
    url(r'^%s/join_request_process/%s$' % (T, JR),  'join_request_process'),

    url(r'^%s/remove_requests$' % T,                'remove_requests'),
)


