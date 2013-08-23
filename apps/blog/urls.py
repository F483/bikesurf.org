# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"


T = "(?P<team_link>%s)" % SLUG # Team Link
B = "(?P<blog_id>%s)" % ID


urlpatterns = patterns("apps.blog.views",
    url(r"^%s$" % T,                     "listing"),
    url(r"^%s/$" % T,                    "listing"),
    url(r"^%s/blog$" % T,                "listing"),
    url(r"^%s/blog/create$" % T,         "create"),
    url(r"^%s/blog/edit/%s$" % (T, B),   "edit"),
    url(r"^%s/blog/delete/%s$" % (T, B), "delete"),
)

