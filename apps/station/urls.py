# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"

T = "(?P<team_link>%s)" % SLUG
S = "(?P<station_id>%s)" % ID


urlpatterns = patterns("apps.station.views",
    url(r"^stations$",                              "listing"),
    url(r"^station/view/%s$" % S,                   "view", { "tab" : "OVERVIEW" }),
    url(r"^station/view/%s/bikes$" % S,             "view", { "tab" : "BIKES" }),
    url(r"^station/view/%s/outgoing$" % S,          "view", { "tab" : "OUTGOING" }),
    url(r"^station/view/%s/incoming$" % S,          "view", { "tab" : "INCOMING" }),
    url(r"^%s/stations$" % T,                       "listing"),
    url(r"^%s/station/create$" % T,                 "create"),
    url(r"^%s/station/edit/%s$" % (T, S),           "edit"),
    url(r"^%s/station/delete/%s$" % (T, S),         "delete"),
    url(r"^%s/station/view/%s$" % (T, S),           "view", { "tab" : "OVERVIEW" }),
    url(r"^%s/station/view/%s/bikes$" % (T, S),     "view", { "tab" : "BIKES" }),
    url(r"^%s/station/view/%s/outgoing$" % (T, S),  "view", { "tab" : "OUTGOING" }),
    url(r"^%s/station/view/%s/incoming$" % (T, S),  "view", { "tab" : "INCOMING" }),
)



