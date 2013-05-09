# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url

SLUG = r"[a-z0-9\-]+"

T = "(?P<team_link>%s)" % SLUG # Team Link
P = "(?P<page_link>%s)" % SLUG # Page Link
CA = "(?P<concerned_id>[0-9]+)" # Concerned Account Link
JR = "(?P<join_request_id>[0-9]+)" # Join Request Link
RR = "(?P<remove_request_id>[0-9]+)" # Remove Request Link


urlpatterns = patterns("apps.team.views",

    url(r"^team/create$",                            "create"),
    url(r"^%s/members$" % T,                         "members"),

    url(r"^%s/join_request/create$" % T,             "join_request_create"),
    url(r"^%s/join_request/created$" % T,            "join_request_created"),
    url(r"^%s/join_request/list$" % T,               "join_request_list"),
    url(r"^%s/join_request/process/%s$" % (T, JR),   "join_request_process"),

    url(r"^%s/remove_request/%s$" % (T, CA),         "remove_request"),
    url(r"^%s/remove_requested$" % T,                "remove_requested"),
    url(r"^%s/remove_requests$" % T,                 "remove_requests"),
    url(r"^%s/remove_request_process/%s$" % (T, RR), "remove_request_process"),
)


