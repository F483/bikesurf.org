# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"

T = "(?P<team_link>%s)" % SLUG
S = "(?P<station_id>%s)" % ID


urlpatterns = patterns("apps.station.views",
    url(r"^stations$",                    "list_my"),
    url(r"^station/view/%s" % S,          "view_my"),
    url(r"^%s/stations$" % T,             "list_team"),
    url(r"^%s/station/create$" % T,       "create"),
    url(r"^%s/station/view/%s$" % (T, S), "view_team"),
)



