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


class Link(Model):

    site        = CharField(max_length=64, choices=SITE_CHOICES)
    profile     = CharField(max_length=1024)

    # metadata
    created_by  = ForeignKey('account.Account', related_name="links_created")
    created_on  = DateTimeField(auto_now_add=True)
    updated_by  = ForeignKey("account.Account", related_name="links_updated")
    updated_on  = DateTimeField(auto_now=True)


