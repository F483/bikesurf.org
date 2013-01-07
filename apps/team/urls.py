# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url

SLUG = r"[a-z0-9\-]+"

T = "(?P<team_link>%s)" % SLUG # Team Link
P = "(?P<page_link>%s)" % SLUG # Page Link
JR = "(?P<join_request_id>[0-9]+)" # Join Request Link


urlpatterns = patterns("apps.team.views",

    url(r"^team/create$",                           "create"),
    url(r"^%s/members$" % T,                        "members"),

    url(r"^%s/join_request$" % T,                   "join_request"),
    url(r"^%s/join_requested$" % T,                 "join_requested"),
    url(r"^%s/join_requests$" % T,                  "join_requests"),
    url(r"^%s/join_request_process/%s$" % (T, JR),  "join_request_process"),

    url(r"^%s/remove_requests$" % T,                "remove_requests"),
)


