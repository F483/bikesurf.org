# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from apps.common.shortcuts import render_response
from apps.account.models import Account
from apps.team.models import Team
from apps.team.models import Page
from apps.team.models import Blog
from apps.team.models import Station


def _is_member(user, team):
    return len(Account.objects.filter(user=user, team=team)) == 1


def _get_team_menue(team, current):
    make_url = lambda pl: '/%s/%s' % (team.link, pl)
    menu = [
        (make_url('blog'), _('BLOG'), current == 'blog', False), 
        (make_url('bikes'), _('BIKES'), current == 'bikes', False), 
        (make_url('members'), _('MEMBERS'), current == 'members', False), 
        (make_url('stations'), _('STATIONS'), current == 'stations', True),
    ]
    pages = team.pages.all()
    menu += map(lambda p: (make_url(p.link), p.name, p.link == current, False), pages)
    return menu


def create(request):
    # TODO
    return render_response(request, 'team/create.html', {})


def blog(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'blog')
    blogs = Blog.objects.all()
    args = { 'current_team' : team, 'team_menu' : menu, 'blogs' : blogs }
    return render_response(request, 'team/blog.html', args)


def _get_bike_filters(request, form):
    # filters 
    #  date from and to
    #  active (only members)
    #  reserve (only members)
    #  kind (default all)
    #  gender (default all)
    #  size (default all)
    #  lights (default all)
    #  fenders (default all)
    #  rack (default all)
    #  basket (default all)
    return {}


def bikes(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'bikes')
    filters = _get_bike_filters(request, None)
    bikes = team.bikes.filter(**filters)
    args = { 'current_team' : team, 'team_menu' : menu, 'bikes' : bikes }
    return render_response(request, 'team/bikes.html', args)


def stations(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    if not _is_member(request.user, team):
        raise PermissionDenied
    menu = _get_team_menue(team, 'stations')
    stations = Station.objects.filter(owner__team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'stations' : stations }
    return render_response(request, 'team/stations.html', args)


def members(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'members')
    members = team.members.all()
    args = { 'current_team' : team, 'team_menu' : menu, 'members' : members }
    return render_response(request, 'team/members.html', args)


def page(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    page = get_object_or_404(Page, link=page_link, team=team)
    menu = _get_team_menue(team, page.link)
    args = { 'current_team' : team, 'team_menu' : menu, 'page' : page }
    return render_response(request, 'team/page.html', args)


