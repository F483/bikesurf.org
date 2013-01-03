# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF
from apps.common.shortcuts import HUMAN_LINK_LEN as HLL


class Page(models.Model):

    team        = models.ForeignKey("team.Team", related_name="pages")
    link        = models.CharField(max_length=128, validators=[RegexValidator("^%s$" % HLF)])
    name        = models.CharField(max_length=1024)
    content     = models.TextField() # TODO make wiki or markdown
    order       = models.IntegerField() # TODO allow None

    # meta
    created_by  = models.ForeignKey("account.Account", related_name="pages_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey("account.Account", related_name="pages_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (("team", "name"), ("team", "link")) 
        ordering = ["order", "created_on"]


