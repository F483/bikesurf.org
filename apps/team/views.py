# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import re
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from apps.common.shortcuts import render_response
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF
from django.contrib.auth.decorators import login_required
from apps.account.models import Account
from apps.team.models import Team
from apps.team.models import Page
from apps.team.models import Blog
from apps.team.models import Station
from apps.team.models import JoinRequest
from apps.team.models import RemoveRequest
from apps.borrow.models import Borrow
from apps.team.forms import CreateTeamForm


def _is_member(user, team):
    return len(Account.objects.filter(user=user, team=team)) == 1


def _get_team_menue(team, current):
    make_url = lambda pl: '/%s/%s' % (team.link, pl)
    menu = [ 
        # URL                           LABEL                   SELECTED                        MEMBERS_ONLY
        (make_url('blog'),              _('BLOG'),              current == 'blog',              False), 
        (make_url('bikes'),             _('BIKES'),             current == 'bikes',             False), 
        (make_url('members'),           _('MEMBERS'),           current == 'members',           False), 
        (make_url('borrows'),           _('BORROWS'),           current == 'borrows',           True),
        (make_url('stations'),          _('STATIONS'),          current == 'stations',          True),
        (make_url('join_requests'),     _('JOIN_REQUESTS'),     current == 'join_requests',     True),
        (make_url('remove_requests'),   _('REMOVE_REQUESTS'),   current == 'remove_requests',   True),
    ]
    pages = team.pages.all()
    menu += map(lambda p: (make_url(p.link), p.name, p.link == current, False), pages)
    return menu


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():

            # get data
            link = form.cleaned_data['link'].strip()
            name = form.cleaned_data['name'].strip()
            country = form.cleaned_data['country']

            # check data
            data_ok = True
            if bool(len(Team.objects.filter(link=link))):
                form.errors['link'] = [_("LINK_USED")]
                data_ok = False
            if not re.match("^%s$" % HLF, link):
                form.errors['link'] = [_("LINK_BAD_FORMAT")]
                data_ok = False
            if bool(len(Team.objects.filter(name=name))):
                form.errors['name'] = [_("NAME_USED")]
                data_ok = False

            # create team
            if data_ok:
                team = Team()
                team.link = link
                team.name = name
                account = get_object_or_404(Account, user=request.user)
                team.created_by = account
                team.updated_by = account
                team.save()
                return HttpResponseRedirect("/%s" % link)
    else:
        form = CreateTeamForm()
    return render_response(request, 'team/create.html', { 'form' : form })


@require_http_methods(['GET'])
def blog(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'blog')
    blogs = Blog.objects.filter(team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'blogs' : blogs }
    return render_response(request, 'team/blog.html', args)


@login_required
@require_http_methods(['GET'])
def join_requests(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    if not _is_member(request.user, team):
        raise PermissionDenied
    menu = _get_team_menue(team, 'join_requests')
    join_requests = JoinRequest.objects.filter(team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'join_requests' : join_requests }
    return render_response(request, 'team/join_requests.html', args)


@login_required
@require_http_methods(['GET'])
def remove_requests(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    if not _is_member(request.user, team):
        raise PermissionDenied
    menu = _get_team_menue(team, 'remove_requests')
    remove_requests = RemoveRequest.objects.filter(team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'remove_requests' : remove_requests }
    return render_response(request, 'team/remove_requests.html', args)


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


@require_http_methods(['GET'])
def bikes(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'bikes')
    filters = _get_bike_filters(request, None)
    bikes = team.bikes.filter(**filters)
    args = { 'current_team' : team, 'team_menu' : menu, 'bikes' : bikes }
    return render_response(request, 'team/bikes.html', args)


@login_required
@require_http_methods(['GET'])
def borrows(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    if not _is_member(request.user, team):
        raise PermissionDenied
    menu = _get_team_menue(team, 'borrows')
    borrows = Borrow.objects.filter(bike__team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'borrows' : borrows }
    return render_response(request, 'team/borrows.html', args)


@login_required
@require_http_methods(['GET'])
def stations(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    if not _is_member(request.user, team):
        raise PermissionDenied
    menu = _get_team_menue(team, 'stations')
    stations = Station.objects.filter(owner__team=team)
    args = { 'current_team' : team, 'team_menu' : menu, 'stations' : stations }
    return render_response(request, 'team/stations.html', args)


@require_http_methods(['GET'])
def members(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    menu = _get_team_menue(team, 'members')
    members = team.members.all()
    args = { 'current_team' : team, 'team_menu' : menu, 'members' : members }
    return render_response(request, 'team/members.html', args)


@require_http_methods(['GET'])
def page(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    page = get_object_or_404(Page, link=page_link, team=team)
    menu = _get_team_menue(team, page.link)
    args = { 'current_team' : team, 'team_menu' : menu, 'page' : page }
    return render_response(request, 'team/page.html', args)


