# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"


T = "(?P<team_link>%s)" % SLUG # Team Link
P = "(?P<page_link>%s)" % SLUG # Page Link


urlpatterns = patterns("apps.page.views",
    url(r"^%s/page/create$" % T,         "create"),
    url(r"^%s/page/edit/%s$" % (T, P),   "edit"),
    url(r"^%s/page/delete/%s$" % (T, P), "delete"),
    url(r"^%s/%s$" % (T, P),             "view"),
)


