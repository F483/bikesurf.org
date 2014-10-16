# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from apps.page.models import Page
from apps.common.shortcuts import uslugify
from apps.team.utils import assert_member


def create(account, team, name, content, order):
    assert_member(account, team)
    page = Page()
    page.team = team
    page.name = name
    page.link = uslugify(name)
    page.content = content
    page.order = order
    page.created_by = account
    page.updated_by = account
    page.save()
    return page


def edit(account, page, name, content, order):
    assert_member(account, page.team)
    page.name = name
    page.content = content
    page.order = order
    page.updated_by = account
    page.save()
    return page


def delete(account, page):
    assert_member(account, page.team)
    page.delete()


