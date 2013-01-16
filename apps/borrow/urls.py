# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url


SLUG = r"[a-z0-9\-]+"
ID = r"[0-9]+"


p = {
    "team" : "(?P<team_link>%s)" % SLUG,
    "bike" : "(?P<bike_id>%s)" % ID,
    "borrow" : "(?P<borrow_id>%s)" % ID,
}


urlpatterns = patterns("apps.borrow.views",
    url(r"^borrows$",                                "list_my"),
    url(r"^borrow/view/%(borrow)s$" % p,             "view_my"),
    url(r"^borrow/cancel/%(borrow)s$" % p,           "cancel_my"),
    url(r"^borrow/rate/%(borrow)s$" % p,             "rate_my"),  # TODO
    url(r"^%(team)s/borrows$" % p,                   "list_team"),
    url(r"^%(team)s/borrow/view/%(borrow)s$" % p,    "view_team"),
    url(r"^%(team)s/borrow/respond/%(borrow)s$" % p, "respond"),
    url(r"^%(team)s/borrow/create/%(bike)s$" % p,    "create"),
    url(r"^%(team)s/borrow/cancel/%(borrow)s$" % p,  "cancel_team"),
    url(r"^%(team)s/borrow/rate/%(borrow)s$" % p,    "rate_team"), # TODO
)


