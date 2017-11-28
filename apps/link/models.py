# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import DateTimeField
from django.utils.translation import ugettext as _
from apps.account.models import Account


SITE_CHOICES = [
    ("COUCHSURFING", _("COUCHSURFING")),
    ("BEWELCOME", _("BEWELCOME")),
    ("FACEBOOK", _("FACEBOOK")),
    ("TWITTER", _("TWITTER")),
]

SITE_IMAGES = { 
    "FACEBOOK" : "/static/link/facebook.png",
    "TWITTER" : "/static/link/twitter.png",
    "COUCHSURFING" : "/static/link/couchsurfing.png",
    "BEWELCOME" : "/static/link/bewelcome.png",
}

VALID_SITE_URLS = { # TODO better match for each site profile patterns
    "FACEBOOK" : [
        "^facebook\.com/",
        "^www\.facebook\.com/",
        "^http://facebook\.com/",
        "^http://www\.facebook\.com/",
        "^https://facebook\.com/",
        "^https://www\.facebook\.com/",
    ],
    "TWITTER" : [
        "^twitter\.com/",
        "^www\.twitter\.com/",
        "^http://twitter\.com/",
        "^http://www\.twitter\.com/",
        "^https://twitter\.com/",
        "^https://www\.twitter\.com/",
    ],
    "BEWELCOME" : [
        "^bewelcome\.org/",
        "^www\.bewelcome\.org/",
        "^http://bewelcome\.org/",
        "^http://www\.bewelcome\.org/",
        "^https://bewelcome\.org/",
        "^https://www\.bewelcome\.org/",
    ],
    "COUCHSURFING" : [
        "^couchsurfing\.org/",
        "^www\.couchsurfing\.org/",
        "^http://couchsurfing\.org/",
        "^http://www\.couchsurfing\.org/",
        "^https://couchsurfing\.org/",
        "^https://www\.couchsurfing\.org/",
        "^couchsurfing\.com/",
        "^www\.couchsurfing\.com/",
        "^http://couchsurfing\.com/",
        "^http://www\.couchsurfing\.com/",
        "^https://couchsurfing\.com/",
        "^https://www\.couchsurfing\.com/"
    ],
}

class Link(Model):

    site       = CharField(max_length=64, choices=SITE_CHOICES)
    profile    = CharField(max_length=1024) # THE ACTUAL URL, BE CAREFUL !!!

    # TODO implement and use mn relationship (the more confirms the better ...)
    confirmed  = ForeignKey(Account,     # None or the account that
                            blank=True, null=True)

    # metadata
    created_by = ForeignKey(Account, related_name="links_created")
    created_on = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey(Account, related_name="links_updated")
    updated_on = DateTimeField(auto_now=True)

    def get_url(self):
        return self.profile

    def get_label(self):
        for site_choice in SITE_CHOICES:
            if site_choice[0] == self.site:
                return site_choice[1]
        raise Exception("Error this should be unreachable!")

    def get_image(self):
        return SITE_IMAGES[self.site]

