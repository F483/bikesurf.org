# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import DateTimeField
from django.utils.translation import ugettext as _


SITE_CHOICES = [
    ("FACEBOOK", _("FACEBOOK")),
    ("TWITTER", _("TWITTER")),
    ("COUCHSURFING", _("COUCHSURFING")),
    ("BEWELCOME", _("BEWELCOME")),
]

SITE_IMAGES = { # TODO correct images hosted localy
    "FACEBOOK" : "http://icons.iconarchive.com/icons/yootheme/social-bookmark/16/social-facebook-box-blue-icon.png",
    "TWITTER" : "http://icons.iconarchive.com/icons/yootheme/social-bookmark/16/social-facebook-box-blue-icon.png",
    "COUCHSURFING" : "http://icons.iconarchive.com/icons/yootheme/social-bookmark/16/social-facebook-box-blue-icon.png",
    "BEWELCOME" : "http://icons.iconarchive.com/icons/yootheme/social-bookmark/16/social-facebook-box-blue-icon.png",
}

SITE_URLS = {
    "FACEBOOK" : "https://www.facebook.com/%s",
    "TWITTER" : "https://twitter.com/%s"
    "BEWELCOME" : "https://www.bewelcome.org/members/%s",
    "COUCHSURFING" : "https://www.couchsurfing.org/profile.html?id=%s",
}

class Link(Model):

    site       = CharField(max_length=64, choices=SITE_CHOICES)
    profile    = CharField(max_length=1024)
    confirmed  = ForeignKey('account.Account',     # None or the account that
                            blank=True, null=True) # confirmed # TODO implement

    # metadata
    created_by = ForeignKey('account.Account', related_name="links_created")
    created_on = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey("account.Account", related_name="links_updated")
    updated_on = DateTimeField(auto_now=True)

    def get_url(self):
        return SITE_URLS[self.site] % self.profile # TODO protect against cross site scripting and js injection

    def get_label(self):
        for site_choice in SITE_CHOICES:
            if site_choice[0] == self.site:
                return site_choice[1]
        raise Exception("Error this should be unreachable!")

    def get_image(self):
        return SITE_IMAGES[self.site]

