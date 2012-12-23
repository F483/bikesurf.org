# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.team.models import Team


class TeamSelectForm(forms.Form):

    team = forms.ModelChoiceField(label='', empty_label=_("WHERE?"), queryset=Team.objects.all()) 
