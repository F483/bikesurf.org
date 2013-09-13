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
    return "team/%s.%s" % (instance.link, 'png')


class Team(Model):

    link        = SlugField(unique=True) # team url name 
    links       = ManyToManyField('link.Link', null=True, blank=True) # team social media links
    name        = CharField(max_length=1024, unique=True)
    country     = CountryField()
    members     = ManyToManyField('account.Account', null=True, blank=True, 
                                  related_name="teams") 
    logo        = ProcessedImageField(upload_to=_upload_to, 
                                      processors=[ResizeToFill(525, 100)],
                                      format='PNG', options={'quality': 90})
    active      = BooleanField(default=False)
    application = TextField() 

    # meta
    created_by  = ForeignKey('account.Account', related_name='team_created')
    created_on  = DateTimeField(auto_now_add=True)
    updated_by  = ForeignKey('account.Account', related_name='team_updated')
    updated_on  = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.country.name)

    class Meta:
        
        ordering = ['name']


class JoinRequest(Model):

    # main data
    team = ForeignKey( # team user wants to join
        'team.Team', related_name='join_requests'
    )
    requester = ForeignKey( # user who is requesting to join
        'account.Account', related_name='join_requests_made'
    ) 
    processor = ForeignKey( # user who answerd the request
        'account.Account', related_name='join_requests_processed', 
        null=True, blank=True
    )
    status = CharField(
        max_length=256, choices=STATUS_CHOICES, default='PENDING'
    )
    application = TextField() # reason given by user to join
    response = TextField(blank=True) # reason given by processor

    # meta
    # created_by = requester
    # updated_by = processor
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s > %s (%s)" % (self.requester, self.team, self.status)

    class Meta:
        
        ordering = ['-status', 'created_on']


class RemoveRequest(Model):

    # main data
    team = ForeignKey( # team to remove user from
        'team.Team', 
        related_name='remove_requests'
    )
    concerned = ForeignKey( # user to be removed
        'account.Account', related_name='remove_requests_concerned'
    )
    requester = ForeignKey( # user who is requesting the removel
        'account.Account', related_name='remove_requests_made'
    )
    processor = ForeignKey( # user who processed the request
        'account.Account', related_name='remove_requests_processed', 
        null=True, blank=True
    )
    status = CharField(
        max_length=256, choices=STATUS_CHOICES, default='PENDING'
    )
    reason = TextField() # reason given by by the requester
    response = TextField(blank=True) # reason given by processor

    # meta
    # created_by = requester
    # updated_by = processor
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s < %s (%s)" % (self.concerned, self.team, self.status)

    class Meta:

        ordering = ['-status', 'created_on']


