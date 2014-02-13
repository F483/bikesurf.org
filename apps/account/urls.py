# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug, arg_username


L = arg_id("link_id")
U = arg_username("username")


urlpatterns = patterns("apps.account.views",
    url(r"^account/profile$",            "profile"),
    url(r"^account/view/%s$" % U,        "view"),
    url(r"^account/set_passport$",       "set_passport", { "wizard" : False }),
    url(r"^account/edit$",               "edit",         { "wizard" : False }),
    url(r"^account/link/create$",        "link_create",  { "wizard" : False }),
    url(r"^account/link/delete/%s$" % L, "link_delete"),

    # this url because allauth
    url(r"^accounts/profile/$",          "edit",         { "wizard" : True }),
    url(r"^account/wiz/link",            "link_create",  { "wizard" : True }),
    url(r"^account/wiz/passport",        "set_passport", { "wizard" : True }),
)

