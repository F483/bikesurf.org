# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from apps.common.shortcuts import render_response
from apps.team.models import Team
from apps.team.models import Page
from apps.team.models import Blog


def _get_team_menue(team, current):
    fixed = ['blog', 'bikes', 'members']
    pages = team.pages.all()
    make_url = lambda pl: '/%s/%s' % (team.link, pl)
    menu  = map(lambda pl: (make_url(pl), _(pl.upper()), pl == current), fixed)
    menu += map(lambda p: (make_url(p.link), p.name, p.link == current), pages)
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


