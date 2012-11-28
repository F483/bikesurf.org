# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext as _
from django_countries import CountryField


SOURCES = [
    'OTHER',
    'COUCHSURFING',
    'FACEBOOK',
    'FRIENDS',
    'GOOGLE',
    'TWITTER',
]
SOURCES_CHOICES = [(source, _(source)) for source in SOURCES]


SITES = [ # TODO add url validation functions per site
    'COUCHSURFING',
    'FACEBOOK',
    'TWITTER',
    'GOOGLEPLUS',
    'BLOG',
    'SKYPE',
]
SITE_CHOICES = [(site, _(site)) for site in SITES]


class Account(models.Model):

    # main data
    user         = models.ForeignKey('auth.User', unique=True)
    description  = models.TextField()
    country      = CountryField()
    source       = models.CharField(max_length=256, choices=SOURCES_CHOICES, default='OTHER')
    feedback     = models.TextField()
    mobile       = models.CharField(max_length=1024)

    # bike sharing teams
    is_team      = models.BooleanField(default=False)
    members      = models.ManyToManyField('self')

    # meta
    created_on   = models.DateTimeField(auto_now_add=True)
    updated_on   = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_team)
        return u"id: %s; user_id: %s; is_team: %s" % args


class Site(models.Model):

    account     = models.ForeignKey('account.Account')
    site        = models.CharField(max_length=256, choices=SITE_CHOICES)
    link        = models.URLField()
    confirmed   = models.BooleanField(default=False) # done by bike lender

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (self.id, self.account.id, self.site, self.confirmed)
        return u"id: %s; account_id: %s; site: %s; confirmed: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('account', 'site'),) 


