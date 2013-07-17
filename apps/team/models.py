# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import SlugField
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import ManyToManyField
from django.db.models import ForeignKey
from django.db.models import DateTimeField
from django.db.models import TextField
from django.utils.translation import ugettext as _
from django_countries import CountryField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


STATUSES = [
    'PENDING',
    'ACCEPTED',
    'DECLINED',
]
STATUS_CHOICES = [(request, _(request)) for request in STATUSES]


def _upload_to(instance, filename, **kwargs):
    return "team/%s.%s" % (instance.link, 'jpeg')


class Team(Model):

    link        = SlugField(unique=True)
    name        = CharField(max_length=1024, unique=True)
    country     = CountryField()
    members     = ManyToManyField('account.Account', null=True, blank=True) 
    logo        = ProcessedImageField(upload_to=_upload_to, 
                                      processors=[ResizeToFill(270, 100)],
                                      format='JPEG', options={'quality': 90})
    active      = BooleanField(default=False)
    application = TextField() 

    # meta
    created_by  = ForeignKey('account.Account', related_name='team_created')
    created_on  = DateTimeField(auto_now_add=True)
    updated_by  = ForeignKey('account.Account', related_name='team_updated')
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:                                                                                                 
                                                                                                                
        ordering = ['name']


class JoinRequest(Model):

    # main data
    team        = ForeignKey('team.Team', related_name='join_requests') # team user wants to join
    requester   = ForeignKey('account.Account', related_name='join_requests_made') # user who is requesting to join
    processor   = ForeignKey('account.Account', related_name='join_requests_processed', null=True, blank=True) # user who answerd the request
    status      = CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    application = TextField() # reason given by user to join
    response    = TextField(blank=True) # reason given by processor

    # meta
    created_on  = DateTimeField(auto_now_add=True)
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s > %s (%s)" % (self.requester, self.team, self.status)

    class Meta:                                                                                                 
                                                                                                                
        ordering = ['-status', 'updated_on']


class RemoveRequest(Model):

    # main data
    team        = ForeignKey('team.Team', related_name='remove_requests') # team to remove user from
    concerned   = ForeignKey('account.Account', related_name='remove_requests_concerned') # user to be removed
    requester   = ForeignKey('account.Account', related_name='remove_requests_made') # user who is requesting the removel
    processor   = ForeignKey('account.Account', related_name='remove_requests_processed', null=True, blank=True) # user who processed the request
    status      = CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    reason      = TextField() # reason given by by the requester
    response    = TextField(blank=True) # reason given by processor

    # meta
    # created_by = requester
    # updated_by = processor
    created_on  = DateTimeField(auto_now_add=True)
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s < %s (%s)" % (self.concerned, self.team, self.status)

    class Meta:

        ordering = ['-status', 'updated_on']


