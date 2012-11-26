# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext as _
from django_countries import CountryField


ROLES = [
    'OWNER',      # can update team data and add remove users/roles
    'MANAGER',    # can lend team bikes to/from team stations
]
ROLE_CHOICES = [(role, _(role)) for role in ROLES]


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


class Cyclist(models.Model):

    # main data
    user         = models.ForeignKey('auth.User', unique=True)
    is_team      = models.BooleanField(default=False)
    description  = models.TextField()
    country      = CountryField()
    source       = models.CharField(max_length=256, choices=SOURCES_CHOICES, default='OTHER')
    feedback     = models.TextField()
    mobile       = models.CharField(max_length=1024)

    # meta
    created_on   = models.DateTimeField(auto_now_add=True)
    updated_on   = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_team)
        return u"id: %s; user_id: %s; is_team: %s" % args


class Profile(models.Model):

    cyclist     = models.ForeignKey('cyclist.Cyclist')
    site        = models.CharField(max_length=256, choices=SITE_CHOICES)
    link        = models.URLField()
    confirmed   = models.BooleanField(default=False) # done by bike lender

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (self.id, self.cyclist.id, self.site, self.confirmed)
        return u"id: %s; cyclist_id: %s; site: %s; confirmed: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('cyclist', 'site'),) 


class Member(models.Model):

    member      = models.ForeignKey('cyclist.Cyclist', related_name='teams')
    team        = models.ForeignKey('cyclist.Cyclist', related_name='members')
    role        = models.CharField(max_length=256, choices=ROLE_CHOICES)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.member.id, self.team, self.role)
        return u"id: %s; memeber_id: %s; team_id: %s; role: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('member', 'team', 'role'),) 


