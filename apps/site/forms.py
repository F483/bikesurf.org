# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.forms import Select
from django.forms import Form
from django.forms import ModelChoiceField
from apps.team.models import Team


class TeamSelectForm(Form):

    team = ModelChoiceField(
            label='', empty_label=_("PICK_A_LOCATION"), 
            queryset=Team.objects.filter(active=True),
            widget=Select(attrs={'style':'WIDTH: 350px;'})
    ) 


