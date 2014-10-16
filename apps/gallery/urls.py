# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug


P = arg_id("picture_id")
G = arg_id("gallery_id")
T = arg_slug("team_link")


urlpatterns = patterns("apps.gallery.views",
    url(r"^gallery/setprimary/%s$" % P,         "setprimary"), # update primary picture
    url(r"^gallery/add/%s$" % G,                "add"),        # add picture to gallery
    url(r"^gallery/remove/%s$" % P,             "remove"),     # remove gallery picture
    url(r"^gallery/list/%s$" % G,               "listing"),    # view gallery
    url(r"^gallery/view/%s$" % P,               "view"),       # view picture

    url(r"^%s/gallery/setprimary/%s$" % (T, P), "setprimary"), # update primary picture
    url(r"^%s/gallery/add/%s$" % (T, G),        "add"),        # add picture to gallery
    url(r"^%s/gallery/remove/%s$" % (T, P),     "remove"),     # remove gallery picture
    url(r"^%s/gallery/list/%s$" % (T, G),       "listing"),    # view gallery
    url(r"^%s/gallery/view/%s$" % (T, P),       "view"),       # view picture
)


