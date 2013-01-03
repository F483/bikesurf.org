# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF


T = "(?P<team_link>%s)" % HLF # Team Link
P = "(?P<page_link>%s)" % HLF # Page Link


urlpatterns = patterns("apps.page.views",
    url(r"^%s/page/create$" % T, "create"),
    url(r"^%s/%s$" % (T, P),     "view"),
)


