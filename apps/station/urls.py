# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"

T = "(?P<team_link>%s)" % SLUG # Team Link


urlpatterns = patterns("apps.station.views",
    url(r"^%s/stations$" % T,       "list"),
    url(r"^%s/station/create$" % T, "create"),
)



