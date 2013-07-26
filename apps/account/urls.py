# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


ID = r"[0-9]+"

p = {
    "link" : "(?P<link_id>%s)" % ID,
}

urlpatterns = patterns("apps.account.views",
    url(r"^accounts/profile/$",                 "view"), # use this url because of allauth
    url(r"^account/edit$",                      "edit"),
    url(r"^account/link/create",                "link_create"),
    url(r"^account/link/delete/%(link)s" % p,   "link_delete")
)

