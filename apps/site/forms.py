# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from apps.account.models import Account


class TeamSelectForm(forms.Form):

    team = forms.ModelChoiceField(
                label='',
                queryset=Account.objects.filter(is_team=True)
            ) 
