# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from sanitizer.models import SanitizedCharField
from config.settings import SANITIZER_ALLOWED_TAGS, SANITIZER_ALLOWED_ATTRIBUTES
from apps.account.models import Account


class Page(models.Model):

    team        = models.ForeignKey("team.Team", related_name="pages")
    link        = models.SlugField(unique=True)
    name        = models.CharField(max_length=1024)
    content     = SanitizedCharField(
                    max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS, 
                    allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, strip=False
                )

    order       = models.IntegerField(blank=True, null=True)

    # meta
    created_by  = models.ForeignKey(Account, related_name="pages_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey(Account, related_name="pages_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (("team", "name"), ("team", "link")) 
        ordering = ["order", "name"]


