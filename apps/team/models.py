# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from common.shortcuts import MODEL_NAME


STATUSES = [
    'PENDING',
    'ACCEPTED',
    'DECLINED',
]
STATUS_CHOICES = [(request, _(request)) for request in STATUSES]


class Team(models.Model):

    name        = MODEL_NAME
    header      = models.TextField(null=True, blank=True) # TODO make wiki or markdown
    members     = models.ManyToManyField('account.Account', null=True, blank=True) 
    country     = CountryField()

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='team_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='team_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s" % self.name


class JoinRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='join_requests') # team user wants to join
    requester   = models.ForeignKey('account.Account', related_name='join_requests_made') # user who is requesting to join
    processor   = models.ForeignKey('account.Account', related_name='join_requests_processed') # user who answerd the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    application = models.TextField() # reason given by user to join
    response    = models.TextField() # reason given by processor

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.team.id, self.requester.id)
        return u"id: %s; team_id: %s; requester_id: %s" % args


class RemoveRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='remove_requests') # team to remove user from
    concerned   = models.ForeignKey('account.Account', related_name='remove_requests_concerned') # user to be removed
    requester   = models.ForeignKey('account.Account', related_name='remove_requests_made') # user who is requesting the removel
    processor   = models.ForeignKey('account.Account', related_name='remove_requests_processed') # user who processed the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    reason      = models.TextField() # reason given by by the requester
    response    = models.TextField() # reason given by processor

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.team.id, self.concerned.id)
        return u"id: %s; team_id: %s; concerned_id: %s" % args


class Page(models.Model): # TODO i18n

    team        = models.ForeignKey('team.Team', related_name='pages')
    name        = MODEL_NAME
    content     = models.TextField() # TODO make wiki or markdown
    is_blog     = models.BooleanField(default=True) # shown in blog entries
    order       = models.IntegerField() # TODO allow None

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='pages_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='pages_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.team.name, self.is_blog and _('BLOG') or _('PAGE'), self.name)
        return u"%s (%s): %s" % args

    class Meta:                                                                                                 
                                                                                                                
        #unique_together = (('team', 'language', 'name')) 
        unique_together = (('team', 'name')) 
        ordering = ['order', 'created_on']


