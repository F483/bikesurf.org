# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.core.exceptions import PermissionDenied
from apps.link import control as link_control
from apps.borrow.models import Borrow
from allauth.account.models import EmailAddress
from django.shortcuts import get_object_or_404


def get_email_or_404(account):
    address = get_object_or_404(EmailAddress, user=account.user, primary=True)
    return address.email


def get_staff_emails():
    addresses = EmailAddress.objects.filter(primary=True, user__is_staff=True)
    return [address.email for address in list(addresses)]


def get_superuser_emails():
    addresses = EmailAddress.objects.filter(primary=True, user__is_superuser=True)
    return [address.email for address in list(addresses)]


def set_passport(account, passport):
    if account.passport:
        os.remove(account.passport.path)
    account.passport = passport
    account.save()
    return account


def can_view_account(current_account, view_account):
    if current_account == view_account:
        return True # user can view own account
    if bool(Borrow.objects.filter(team__members=current_account, 
                                  borrower=view_account)):
        return True # user can view if account has borrow from one of there teams
    # TODO allow admins to view everyone
    return False


def edit(account, username, first_name, last_name, mobile, source, description):
    account.user.username = username
    account.user.first_name = first_name
    account.user.last_name = last_name
    account.user.save()
    account.mobile = mobile
    account.source = source
    account.description = description
    account.save()


#########
# LINKS #
#########


def site_link_exists(account, site):
    return bool(list(account.links.filter(site=site)))


def can_create_link(account, site, profile):
    exists = site_link_exists(account, site)
    return link_control.valid_profile_format(profile) and not exists


def can_delete_link(account, link):
    return link in account.links.all()


def link_create(account, site, profile):
    if not can_create_link(account, site, profile):
        raise PermissionDenied
    link = link_control.create(account, site, profile)
    account.links.add(link)


def link_delete(account, link):
    if not can_delete_link(account, link):
        raise PermissionDenied
    account.links.remove(link)
    link.delete()



