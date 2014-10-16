# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from apps.common.urls import arg_id, arg_slug


p = {
    "team" : arg_slug("team_link"),
    "bike" : arg_id("bike_id"),
    "borrow" : arg_id("borrow_id"),
}


urlpatterns = patterns("apps.borrow.views",
    url(r"^borrows$",                                   "borrower_list"),
    url(r"^borrow/arrivals$",                           "arrivals"),
    url(r"^borrow/departures$",                         "departures"),
    url(r"^borrow/view/%(borrow)s$" % p,                "borrower_view"),
    url(r"^borrow/edit/%(borrow)s$" % p,                "borrower_edit"),
    url(r"^borrow/cancel/%(borrow)s$" % p,              "borrower_cancel"),
    url(r"^borrow/rate/%(borrow)s$" % p,                "borrower_rate"),
    url(r"^borrow/comment/%(borrow)s$" % p,             "comment"),

    url(r"^%(team)s/borrows$" % p,                      "lender_list"),
    url(r"^%(team)s/borrow/view/%(borrow)s$" % p,       "lender_view"),
    url(r"^%(team)s/borrow/edit/%(borrow)s$" % p,       "lender_edit"),
    url(r"^%(team)s/borrow/edit_dest/%(borrow)s$" % p,  "lender_edit_dest"),
    url(r"^%(team)s/borrow/respond/%(borrow)s$" % p,    "respond"),
    url(r"^%(team)s/borrow/create/%(bike)s$" % p,       "create"),
    url(r"^%(team)s/borrow/cancel/%(borrow)s$" % p,     "lender_cancel"),
    url(r"^%(team)s/borrow/rate/%(borrow)s$" % p,       "lender_rate"),
    url(r"^%(team)s/borrow/comment/%(borrow)s$" % p,    "comment"),
)


