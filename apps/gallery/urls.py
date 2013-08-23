# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"

P = "(?P<picture_id>%s)" % ID
G = "(?P<gallery_id>%s)" % ID
T = "(?P<team_link>%s)" % SLUG


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


