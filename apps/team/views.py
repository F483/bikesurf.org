# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from common.shortcuts import render_response
from apps.team.models import Team
from apps.team.models import Page


def get_team_menue(team, current):
    pages = team.pages.filter(is_blog=False)
    names = ['blog', 'bikes', 'members'] + map(lambda p: p.name, pages.all())
    make_i18n = lambda name: name.upper() == _(name.upper()) and name or _(name.upper())
    make_url = lambda name: '/team/%s/%s' % (team.name, name)
    make_entry = lambda name: (make_url(name), make_i18n(name), name == current)
    return map(make_entry, names)


def blog(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    menu = get_team_menue(team, 'blog')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/blog.html', args)


def bikes(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    menu = get_team_menue(team, 'bikes')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/bikes.html', args)


def members(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    menu = get_team_menue(team, 'members')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/members.html', args)


def page(request, team_name, page_name):
    team = get_object_or_404(Team, name=team_name)
    page = get_object_or_404(Page, name=page_name, team=team)
    menu = get_team_menue(team, page.name)
    args = { 'current_team' : team, 'team_menu' : menu, 'page' : page }
    return render_response(request, 'team/page.html', args)


