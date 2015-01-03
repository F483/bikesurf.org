# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE.TXT file)


from django.utils.translation import ugettext as _
from django.forms import Select
from django.forms import Form
from django.forms import ModelChoiceField
from django.db.models import Count
from apps.team.models import Team

teams = Team.objects.all().annotate(bike_count=Count("bikes__id"))
teams = teams.filter(active=True, bike_count__gt=0)

class TeamSelectForm(Form):

    team = ModelChoiceField(
        label='', empty_label=_("PICK_A_LOCATION"),
        queryset=teams,
        widget=Select(attrs={'class':'form-control'})
    )


