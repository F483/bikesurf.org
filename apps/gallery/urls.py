# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"

P = "(?P<picture_id>%s)" % ID
G = "(?P<gallery_id>%s)" % ID
T = "(?P<team_link>%s)" % SLUG,


urlpatterns = patterns("apps.gallery.views",
    url(r"^gallery/create$",                  "create"),  # create gallery
    url(r"^gallery/delete/%s$" % G,           "delete"),  # delete gallery
    url(r"^gallery/primary/%s$" % G,          "primary"), # update primary picture
    url(r"^gallery/add/%s$" % G,              "add"),     # add picture to gallery
    url(r"^gallery/remove/%s$" % P,           "remove"),  # remove gallery picture
    url(r"^gallery/update/%s$" % P,           "update"),  # update gallery picture
    url(r"^gallery/list/%s$" % G,             "list"),    # view gallery
    url(r"^gallery/view/%s$" % P,             "view"),    # view picture

    url(r"^%s/gallery/create$" % T,           "create"),  # create gallery
    url(r"^%s/gallery/delete/%s$" % (T, G),   "delete"),  # delete gallery
    url(r"^%s/gallery/primary/%s$" % (T, G),  "primary"), # update primary picture
    url(r"^%s/gallery/add/%s$" % (T, G),      "add"),     # add picture to gallery
    url(r"^%s/gallery/remove/%s$" % (T, P),   "remove"),  # remove gallery picture
    url(r"^%s/gallery/update/%s$" % (T, P),   "update"),  # update gallery picture
    url(r"^%s/gallery/list/%s$" % (T, G),     "list"),    # view gallery
    url(r"^%s/gallery/view/%s$" % (T, P),     "view"),    # view picture
)


