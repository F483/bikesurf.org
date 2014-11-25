# -*- coding: utf-8 -*-
# Copyright (c) 2014 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE.TXT file)

from django.conf import settings as _settings

def settings(request):
  return { 'settings': _settings }

def account(request):
    # avoid circular imports ...
    from apps.team import control as team_control 
    from apps.borrow import control as borrow_control
    from apps.station.models import Station
    if request.user.is_authenticated():
        account = request.user.accounts.all()[0]
        stations = Station.objects.filter(responsible=account)
        return { 
            "current_account" : account,
            "current_account_teams" : team_control.get_teams(account),
            "current_account_stations" : stations,
            "borrow_count" : len(borrow_control.my_borrows(account)),
            "departure_count" : len(borrow_control.departures(account)),
            "arrival_count" : len(borrow_control.arrivals(account)),
        }
    return {}
