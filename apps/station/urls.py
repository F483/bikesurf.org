# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug


T = arg_slug("team_link")
S = arg_id("station_id")


urlpatterns = patterns("apps.station.views",
    url(r"^stations$",                               "listing"),
    url(r"^station/view/%s$" % S,                    "view", { "tab" : "OVERVIEW" }),
    url(r"^station/view/%s/bikes$" % S,              "view", { "tab" : "BIKES" }),
    url(r"^station/view/%s/departures$" % S,         "view", { "tab" : "DEPARTURES" }),
    url(r"^station/view/%s/arrivals$" % S,           "view", { "tab" : "ARRIVALS" }),
    url(r"^%s/stations$" % T,                        "listing"),
    url(r"^%s/station/create$" % T,                  "create"),
    url(r"^%s/station/edit/%s$" % (T, S),            "edit"),
    url(r"^%s/station/delete/%s$" % (T, S),          "delete"),
    url(r"^%s/station/view/%s$" % (T, S),            "view", { "tab" : "OVERVIEW" }),
    url(r"^%s/station/view/%s/bikes$" % (T, S),      "view", { "tab" : "BIKES" }),
    url(r"^%s/station/view/%s/departures$" % (T, S), "view", { "tab" : "DEPARTURES" }),
    url(r"^%s/station/view/%s/arrivals$" % (T, S),   "view", { "tab" : "ARRIVALS" }),
)



