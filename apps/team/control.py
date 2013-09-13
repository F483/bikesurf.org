# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from apps.team.models import Team
from apps.team.models import JoinRequest
from apps.common.shortcuts import uslugify
from apps.team.models import RemoveRequest
from apps.link import control as link_control
from apps.team import signals
from apps.common.shortcuts import send_mail
from apps.account import control as account_control


@receiver(signals.team_created)
def notify_staff_team_created(sender, **kwargs):
    emails = account_control.get_superuser_emails()
    subject = "team/email/notify_staff_team_created_subject.txt"
    message = "team/email/notify_staff_team_created_message.txt"
    send_mail(emails, subject, message, kwargs)


@receiver(signals.join_request_created)
def notify_team_join_request_created(sender, **kwargs):
    join_request = kwargs["join_request"]
    if join_request.status != "PENDING":
        return # requester autojoined an empty team
    emails = get_team_emails(join_request.team)
    subject = "team/email/notify_team_join_request_created_subject.txt"
    message = "team/email/notify_team_join_request_created_message.txt"
    send_mail(emails, subject, message, kwargs)


@receiver(signals.remove_request_created)
def notify_concerned_remove_request_created(sender, **kwargs):
    rr = kwargs["remove_request"]
    if rr.status != "PENDING":
        return # last member was autoremoved
    email = account_control.get_email_or_404(rr.concerned)
    subject = "team/email/notify_concerned_remove_request_created_subject.txt"
    message = "team/email/notify_concerned_remove_request_created_message.txt"
    send_mail([email], subject, message, kwargs)


@receiver(signals.remove_request_created)
def notify_team_remove_request_created(sender, **kwargs):
    rr = kwargs["remove_request"]
    if rr.status != "PENDING":
        return # last member was autoremoved
    emails = get_team_emails(rr.team, excludes=[rr.concerned])
    subject = "team/email/notify_team_remove_request_created_subject.txt"
    message = "team/email/notify_team_remove_request_created_message.txt"
    send_mail(emails, subject, message, kwargs)


def get_team_emails(team, excludes=None):
    qs = EmailAddress.objects.filter(
            primary=True, 
            user__accounts__teams=team
    )
    if excludes:
        for exclude in excludes:
            qs = qs.exclude(user__accounts=exclude)
    return [address.email for address in list(qs)]


def get_teams(account):
    return list(account.teams.filter(active=True))


def get_or_404(link):
    return get_object_or_404(Team, link=link, active=True)


def is_member(account, team):
    return account in team.members.all()


def create(account, name, country, logo, application):
    team = None
    with transaction.commit_on_success():
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
    signals.team_created.send(sender=create, team=team, creator=account)
    return team


########
# LOGO #
########


def can_replace_logo(account, team):
    return is_member(account, team) and team.active == True


def replace_logo(account, team, logo):
    if not can_replace_logo(account, team):
        raise PermissionDenied
    with transaction.commit_on_success():
        os.remove(team.logo.path)
        team.logo = logo
        team.save()
        return team


################
# JOIN REQUEST #
################


def can_join(account, team):
    filters = {"team" : team, "requester" : account, "status" : "PENDING"}
    return ( not is_member(account, team) and 
             not len(JoinRequest.objects.filter(**filters)) > 0 )


def create_join_request(account, team, application):
    if not can_join(account, team):
        raise PermissionDenied
    join_request = None
    with transaction.commit_on_success():
        join_request = JoinRequest()
        join_request.team = team
        join_request.requester = account
        join_request.application = application
        if len(team.members.all()) == 0: # auto join empty teams
            join_request.status = "ACCEPTED"
            team.members.add(account)
        join_request.save()
    signals.join_request_created.send(sender=create_join_request, 
                                      join_request=join_request)
    return join_request


def can_process_join_request(account, join_request):
    return (is_member(account, join_request.team) and
            join_request.status == "PENDING")


def process_join_request(account, join_request, response, status):
    if not can_process_join_request(account, join_request):
        raise PermissionDenied
    with transaction.commit_on_success():
        join_request.processor = account
        join_request.response = response
        join_request.status = status
        join_request.save()
        if join_request.status == 'ACCEPTED':
            join_request.team.members.add(join_request.requester)


##################
# REMOVE REQUEST #
##################


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
    remove_request = None
    with transaction.commit_on_success():
        remove_request = RemoveRequest()
        remove_request.team = team
        remove_request.requester = requester
        remove_request.concerned = concerned
        remove_request.reason = reason
        if len(team.members.all()) == 1: # auto remove last member
            remove_request.status = "ACCEPTED"
            remove_request.team.members.remove(remove_request.concerned)
        remove_request.save()
    signals.remove_request_created.send(sender=create_remove_request, 
                                        remove_request=remove_request)
    return remove_request


def process_remove_request(account, remove_request, response, status):
    if not can_process_remove_request(account, remove_request):
        raise PermissionDenied
    with transaction.commit_on_success():
        remove_request.processor = account
        remove_request.response = response
        remove_request.status = status
        remove_request.save()
        if status == "ACCEPTED":
            remove_request.team.members.remove(remove_request.concerned)


#########
# LINKS #
#########


def site_link_exists(team, site):
    return bool(list(team.links.filter(site=site)))


def can_create_link(account, team, site, profile):
    return (link_control.valid_profile_format(profile) and 
            not site_link_exists(team, site) and is_member(account, team))


def can_delete_link(account, team, link):
    return link in team.links.all() and is_member(account, team)


def link_create(account, team, site, profile):
    if not can_create_link(account, team, site, profile):
        raise PermissionDenied
    link = link_control.create(account, site, profile)
    team.links.add(link)


def link_delete(account, team, link):
    if not can_delete_link(account, team, link):
        raise PermissionDenied
    team.links.remove(link)
    link.delete()



