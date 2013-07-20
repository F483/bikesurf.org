# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from apps.link.models import SITE_CHOICES
from apps.link.models import Link


def can_create(account, site, profile):
    return (account and site and profile and 
            site in [x[0] for x in SITE_CHOICES])


def create(account, site, profile):
    if not can_create(account, site, profile):
        raise PermissionDenied
    link = Link()
    link.site = site
    link.profile = profile
    link.created_by = account
    link.updated_by = account
    link.save()
    return link

