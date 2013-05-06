# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField


STATUSES = [
    'PENDING',
    'ACCEPTED',
    'DECLINED',
]
STATUS_CHOICES = [(request, _(request)) for request in STATUSES]


class Team(models.Model):

    link        = models.SlugField(unique=True)
    name        = models.CharField(max_length=1024, unique=True)
    members     = models.ManyToManyField('account.Account', null=True, blank=True) 
    country     = CountryField()

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='team_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='team_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:                                                                                                 
                                                                                                                
        ordering = ['name']


class JoinRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='join_requests') # team user wants to join
    requester   = models.ForeignKey('account.Account', related_name='join_requests_made') # user who is requesting to join
    processor   = models.ForeignKey('account.Account', related_name='join_requests_processed', null=True, blank=True) # user who answerd the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    application = models.TextField() # reason given by user to join
    response    = models.TextField(blank=True) # reason given by processor

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s > %s (%s)" % (self.requester, self.team, self.status)

    class Meta:                                                                                                 
                                                                                                                
        ordering = ['-status', 'updated_on']


class RemoveRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='remove_requests') # team to remove user from
    concerned   = models.ForeignKey('account.Account', related_name='remove_requests_concerned') # user to be removed
    requester   = models.ForeignKey('account.Account', related_name='remove_requests_made') # user who is requesting the removel
    processor   = models.ForeignKey('account.Account', related_name='remove_requests_processed', null=True, blank=True) # user who processed the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    reason      = models.TextField() # reason given by by the requester
    response    = models.TextField(blank=True) # reason given by processor

    # meta
    # TODO created_by updated_by fields
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s < %s (%s)" % (self.concerned, self.team, self.status)

    class Meta:

        ordering = ['-status', 'updated_on']


