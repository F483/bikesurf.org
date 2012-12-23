# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from common.shortcuts import render_response
from apps.team.models import Team
from apps.team.models import Page


def get_team_menue(team, current):
    fixed = ['blog', 'bikes', 'members']
    pages = team.pages.filter(is_blog=False)
    make_url = lambda pl: '/%s/%s' % (team.link, pl)
    menu  = map(lambda pl: (make_url(pl), _(pl.upper()), pl == current), fixed)
    menu += map(lambda p: (make_url(p.link), p.name, p.link == current), pages)
    return menu


def blog(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = get_team_menue(team, 'blog')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/blog.html', args)


def bikes(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = get_team_menue(team, 'bikes')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/bikes.html', args)


def members(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = get_team_menue(team, 'members')
    args = { 'current_team' : team, 'team_menu' : menu }
    return render_response(request, 'team/members.html', args)


def page(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    page = get_object_or_404(Page, link=page_link, team=team)
    menu = get_team_menue(team, page.link)
    args = { 'current_team' : team, 'team_menu' : menu, 'page' : page }
    return render_response(request, 'team/page.html', args)


