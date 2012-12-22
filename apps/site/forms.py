# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from apps.team.models import Team


class TeamSelectForm(forms.Form):

    team = forms.ModelChoiceField(label='', queryset=Team.objects.all()) 
