# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _
from apps.common.templatetags.common_tags import condition_tag

register = template.Library()

@register.tag
@condition_tag
def if_can_edit_gallery(account, gallery):
    return not ((gallery.team and account not in gallery.team.members.all()) or 
                (not gallery.team and gallery.created_by != account))

