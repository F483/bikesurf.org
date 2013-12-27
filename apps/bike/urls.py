# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug


T = arg_slug("team_link")
B = arg_id("bike_id")


urlpatterns = patterns("apps.bike.views",
    url(r"^%s/bikes$" % T,                      "listing"),
    url(r"^%s/bike/view/%s$" % (T, B),          "view", { "tab" : "OVERVIEW" }),
    url(r"^%s/bike/edit/%s$" % (T, B),          "edit"),
    url(r"^%s/bike/delete/%s$" % (T, B),        "delete"),
    url(r"^%s/bike/view/%s/borrows$" % (T, B),  "view", { "tab" : "BORROWS" }),
    url(r"^%s/bike/create$" % T,                "create"),
)


