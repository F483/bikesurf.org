# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
from django.core.exceptions import PermissionDenied
from apps.link import control as link_control
from apps.borrow.models import Borrow


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
    return True


def edit(account, username, first_name, last_name, mobile, source, description):
    account.user.username = username
    account.user.first_name = first_name
    account.user.last_name = last_name
    account.user.save()
    account.mobile = mobile
    account.source = source
    account.description = description
    account.save()


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



