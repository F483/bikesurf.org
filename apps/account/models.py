# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext as _
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
    description  = models.TextField()
    country      = CountryField()
    source       = models.CharField(max_length=256, choices=SOURCES_CHOICES, default='OTHER')
    feedback     = models.TextField()
    mobile       = models.CharField(max_length=1024)

    # bike sharing teams
    is_team      = models.BooleanField(default=False)
    header       = models.TextField() # TODO make wiki or markdown
    members      = models.ManyToManyField('self')

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='team_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='team_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_team)
        return u"id: %s; user_id: %s; is_team: %s" % args


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
    

