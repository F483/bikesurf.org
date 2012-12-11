# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext as _


STATUSES = [
    'PENDING',
    'ACCEPTED',
    'DECLINED',
]
STATUS_CHOICES = [(request, _(request)) for request in STATUSES]


class JoinRequest(models.Model):

    # main data
    team        = models.ForeignKey('account.Account', related_name='join_requests') # team user wants to join
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
    team        = models.ForeignKey('account.Account', related_name='remove_requests') # team to remove user from
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

    team        = models.ForeignKey('account.Account', related_name='pages')
    url         = models.CharField(max_length=1024) # relative "/team/page/<url>"
    title       = models.CharField(max_length=1024)
    content     = models.TextField() # TODO make wiki or markdown
    #language    = models.CharField(max_length=1024) # TODO language choices

    is_blog     = models.BooleanField(default=True) # shown in blog entries
    order       = models.IntegerField() # TODO allow None

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='pages_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='pages_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.team.id, self.is_blog, self.title)
        return u"id: %s; team_id: %s; is_blog: %s; title: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        #unique_together = (('team', 'language', 'title'), ('team','language',  'url')) 
        unique_together = (('team', 'title'), ('team', 'url')) 


