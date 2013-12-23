# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import re
from django.core.exceptions import PermissionDenied
from apps.link.models import Link
from apps.link.models import SITE_CHOICES, VALID_SITE_URLS


def valid_profile_format(profile, site):
    patterns = VALID_SITE_URLS.get(site)
    if not patterns:
        return False
    for pattern in patterns:
        if bool(re.match(pattern, profile)):
            return True
    return False


def can_create(account, site, profile):
    return (account and site and profile and valid_profile_format(profile, site) 
            and site in [x[0] for x in SITE_CHOICES])


def ensure_https(profile):
    if re.match("^https", profile): # already given
        return profile
    if re.match("^http", profile): # only http
        return "https" + profile[4:]
    return "https://" + profile # nothing


def create(account, site, profile):
    if not can_create(account, site, profile):
        raise PermissionDenied
    link = Link()
    link.site = site
    link.profile = ensure_https(profile)
    link.created_by = account
    link.updated_by = account
    link.save()
    return link

