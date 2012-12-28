# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField


class Account(models.Model):

    SOURCES = [
        'OTHER',
        'COUCHSURFING',
        'FACEBOOK',
        'FRIENDS',
        'GOOGLE',
        'TWITTER',
    ]
    SOURCES_CHOICES = [(source, _(source)) for source in SOURCES]

    # main data
    user         = models.ForeignKey('auth.User', unique=True)
    description  = models.TextField(blank=True)
    source       = models.CharField(max_length=256, choices=SOURCES_CHOICES, default='OTHER')
    feedback     = models.TextField(blank=True)
    mobile       = models.CharField(max_length=1024)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def get_name():
        return self.user.username

    def __unicode__(self):
        return self.user.username

    class Meta:

        ordering = ['user__username']


class Site(models.Model):

    SITES = [ # TODO add url validation functions per site
        'COUCHSURFING',
        'FACEBOOK',
        'TWITTER',
        'GOOGLEPLUS',
        'BLOG',
        'SKYPE',
        'LINKED_IN',
        'BE_WELCOME',
        'WARM_SHOWERS',
        'PINTEREST',
        'YOUTUBE',
    ]
    SITE_CHOICES = [(site, _(site)) for site in SITES]

    # main data
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


class Vacation(models.Model):

    account     = models.ForeignKey('account.Account')
    start       = models.DateField()
    finish      = models.DateField() # inclusive

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.start, self.finish)
        return u"id: %s; user_id: %s; start: %s; finish: %s" % args
    

