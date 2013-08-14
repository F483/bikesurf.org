# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import URLField
from django.db.models import ManyToManyField
from django.utils.translation import ugettext as _
from django_countries import CountryField
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


@receiver(user_signed_up)
def signed_up_callback(sender, **kwargs):
    account = Account()
    account.user = kwargs["user"]
    # TODO preset account.source based on HTTP_REFERER
    account.save()


SOURCE_CHOICES = [
    ('OTHER', _('OTHER')),
    ('COUCHSURFING', _('COUCHSURFING')),
    ('FACEBOOK', _('FACEBOOK')),
    ('FRIENDS', _('FRIENDS')),
    ('GOOGLE', _('GOOGLE')),
    ('TWITTER', _('TWITTER')),
]


def _upload_to(instance, filename, **kwargs):
    return "account/passport/%s.%s" % (instance.id, 'jpeg')


class Account(Model):

    # main data
    user = ForeignKey('auth.User', unique=True, related_name="accounts")
    description = TextField(blank=True)
    source = CharField(max_length=64, choices=SOURCE_CHOICES, default='OTHER')
    mobile = CharField(max_length=1024, blank=True)
    links = ManyToManyField('link.Link', null=True, blank=True) 
    passport = ProcessedImageField(upload_to=_upload_to, null=True, blank=True, 
                                   processors=[ResizeToFill(1024, 768)],
                                   format='JPEG', options={'quality': 90})

    # meta
    # created_by = self
    # updated_by = self
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    def get_name():
        return self.user.username

    def __unicode__(self):
        return self.user.username

    class Meta:

        ordering = ['user__username']


