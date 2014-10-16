# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from apps.link import control as link_control
from apps.borrow.models import Borrow
from apps.account.models import Account
from apps.common.shortcuts import get_object_or_none


def get_site_account():
    site = Site.objects.get_current()
    return get_object_or_none(Account, user__username=site.name)


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
    # TODO allow team members to view own team members
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


###############################
# required borrow information #
###############################

def has_fullname(account):
    return bool(account.user.first_name and account.user.last_name)


def has_mobile(account):
    return bool(account.mobile)


def has_passport(account):
    return bool(account.passport)


def has_required_info(account):
    return (has_fullname(account) and 
            has_mobile(account) and 
            has_passport(account))


#########
# LINKS #
#########


def site_link_exists(account, site):
    return bool(list(account.links.filter(site=site)))


def can_create_link(account, site, profile):
    exists = site_link_exists(account, site)
    return link_control.valid_profile_format(profile, site) and not exists


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



