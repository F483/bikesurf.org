# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


ID = r"[0-9]+"
SLUG = r"[a-z0-9\-]+"

T = "(?P<team_link>%s)" % SLUG # Team Link
P = "(?P<page_link>%s)" % SLUG # Page Link
L = "(?P<link_id>%s)" % ID
CA = "(?P<concerned_id>[0-9]+)" # Concerned Account Link
JR = "(?P<join_request_id>[0-9]+)" # Join Request Link
RR = "(?P<remove_request_id>[0-9]+)" # Remove Request Link


urlpatterns = patterns("apps.team.views",

    url(r"^team/create$",                            "create"),
    url(r"^%s/created$" % T,                         "created"),
    url(r"^%s/members$" % T,                         "members"),
    url(r"^%s/replace_logo$" % T,                    "replace_logo"),
    url(r"^%s/link/create$" % T,                     "link_create"),
    url(r"^%s/link/delete/%s$" % (T, L),             "link_delete"),

    url(r"^%s/join_request/create$" % T,             "join_request_create"),
    url(r"^%s/join_request/created$" % T,            "join_request_created"),
    url(r"^%s/join_request/list$" % T,               "join_request_list"),
    url(r"^%s/join_request/process/%s$" % (T, JR),   "join_request_process"),

    url(r"^%s/remove_request/create/%s$" % (T, CA),  "remove_request_create"),
    url(r"^%s/remove_request/created$" % T,          "remove_request_created"),
    url(r"^%s/remove_request/list$" % T,             "remove_request_list"),
    url(r"^%s/remove_request/process/%s$" % (T, RR), "remove_request_process"),
)


