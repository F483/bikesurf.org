# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"

T = "(?P<team_link>%s)" % SLUG # Team Link


urlpatterns = patterns("apps.bike.views",
    url(r"^%s/bikes$" % T,       "list"),
    url(r"^%s/bike/create$" % T, "create"),
)


