# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from apps.team.utils import assert_member
from apps.blog.models import Blog


def create(account, team, name, content):
    assert_member(account, team)
    blog = Blog()
    blog.team = team
    blog.name = name
    blog.content = content
    blog.created_by = account
    blog.updated_by = account
    blog.save()
    return blog


def edit(account, blog, name, content):
    assert_member(account, blog.team)
    blog.name = name
    blog.content = content
    blog.updated_by = account
    blog.save()
    return blog


def delete(account, blog):
    assert_member(account, blog.team)
    blog.delete()


