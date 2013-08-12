# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.shortcuts import get_object_or_404
from apps.team.models import Team
from apps.team.models import JoinRequest
from django.core.exceptions import PermissionDenied
from apps.common.shortcuts import uslugify
from apps.team.models import RemoveRequest


def get_or_404(link):
    return get_object_or_404(Team, link=link, active=True)


def is_member(account, team):
    return account in team.members.all()


def can_replace_logo(account, team):
    return is_member(account, team) and team.active == True


def replace_logo(account, team, logo):
    if not can_replace_logo(account, team):
        raise PermissionDenied
    os.remove(team.logo.path)
    team.logo = logo
    team.save()
    return team


def create(account, name, country, logo, application):
    team = Team()
    team.name = name
    team.link = uslugify(name)
    team.country = country
    team.logo = logo
    team.application = application
    team.created_by = account
    team.updated_by = account
    team.save()
    team.members.add(account)
    return team


def can_join(account, team):
    filters = {"team" : team, "requester" : account, "status" : "PENDING"}
    return ( not is_member(account, team) and 
             not len(JoinRequest.objects.filter(**filters)) > 0 )


def create_join_request(account, team, application):
    if not can_join(account, team):
        raise PermissionDenied
    join_request = JoinRequest()
    join_request.team = team
    join_request.requester = account
    join_request.application = application
    if len(team.members.all()) == 0: # auto join empty teams
        join_request.status = "ACCEPTED"
        team.members.add(account)
    join_request.save()
    return join_request


def can_process_join_request(account, join_request):
    return (is_member(account, join_request.team) and
            join_request.status == "PENDING")


def process_join_request(account, join_request, response, status):
    if not can_process_join_request(account, join_request):
        raise PermissionDenied
    join_request.processor = account
    join_request.response = response
    join_request.status = status
    join_request.save()
    if join_request.status == 'ACCEPTED':
        join_request.team.members.add(join_request.requester)


def has_remove_request(concerned, team):
    filters = { "team" : team, "concerned" : concerned, "status" : "PENDING"}
    return len(RemoveRequest.objects.filter(**filters)) > 0


def can_create_remove_request(requester, concerned, team):
    return (is_member(requester, team) and is_member(concerned, team) and
            not has_remove_request(concerned, team) and
            not has_remove_request(requester, team))


def can_process_remove_request(account, remove_request):
    return (
        remove_request.status == "PENDING" and # must be pending
        remove_request.concerned != account and # cannot process oneself
        (
            remove_request.requester != account or # requester cant process
            len(remove_request.team.members.all()) == 2 # unless 2 members
        ) and
        is_member(account, remove_request.team) and # processor must be member
        not has_remove_request(account, remove_request.team) # no remove request for processor
    )


def create_remove_request(requester, concerned, team, reason):
    if not can_create_remove_request(requester, concerned, team):
        raise PermissionDenied
    remove_request = RemoveRequest()
    remove_request.team = team
    remove_request.requester = requester
    remove_request.concerned = concerned
    remove_request.reason = reason
    if len(team.members.all()) == 1: # auto remove last member
        remove_request.status = "ACCEPTED"
        remove_request.team.members.remove(remove_request.concerned)
    remove_request.save()
    return remove_request


def process_remove_request(account, remove_request, response, status):
    if not can_process_remove_request(account, remove_request):
        raise PermissionDenied
    remove_request.processor = account
    remove_request.response = response
    remove_request.status = status
    remove_request.save()
    if status == "ACCEPTED":
        remove_request.team.members.remove(remove_request.concerned)


