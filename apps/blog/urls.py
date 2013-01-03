# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF


T = "(?P<team_link>%s)" % HLF # Team Link


urlpatterns = patterns("apps.blog.views",
    url(r"^%s$" % T,             "list"),
    url(r"^%s/$" % T,            "list"),
    url(r"^%s/blog$" % T,        "list"),
    url(r"^%s/blog/create$" % T, "create"),
)

