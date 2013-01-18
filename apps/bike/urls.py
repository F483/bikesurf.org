# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"

T = "(?P<team_link>%s)" % SLUG
B = "(?P<bike_id>%s)" % ID


urlpatterns = patterns("apps.bike.views",
    url(r"^bike/view/%s" % B,         "view_my"),
    url(r"^bikes$",                   "list_my"),
    url(r"^%s/bikes$" % T,            "list_team"),
    url(r"^%s/bike/view/%s" % (T, B), "view_team"),
    url(r"^%s/bike/create$" % T,      "create"),
)


