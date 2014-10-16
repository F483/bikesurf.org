# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug


T = arg_slug("team_link")
B = arg_id("blog_id")


urlpatterns = patterns("apps.blog.views",
    url(r"^%s$" % T,                     "listing"),
    url(r"^%s/$" % T,                    "listing"),
    url(r"^%s/blog$" % T,                "listing"),
    url(r"^%s/blog/create$" % T,         "create"),
    url(r"^%s/blog/edit/%s$" % (T, B),   "edit"),
    url(r"^%s/blog/delete/%s$" % (T, B), "delete"),
)

