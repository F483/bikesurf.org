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
    url(r"^%(team)s/borrow/edit_bike/%(borrow)s$" % p,  "lender_edit_bike"),
    url(r"^%(team)s/borrow/edit_dest/%(borrow)s$" % p,  "lender_edit_dest"),
    url(r"^%(team)s/borrow/respond/%(borrow)s$" % p,    "respond"),
    url(r"^%(team)s/borrow/create/%(bike)s$" % p,       "create"),
    url(r"^%(team)s/borrow/cancel/%(borrow)s$" % p,     "lender_cancel"),
    url(r"^%(team)s/borrow/rate/%(borrow)s$" % p,       "lender_rate"),
    url(r"^%(team)s/borrow/comment/%(borrow)s$" % p,    "comment"),
)


