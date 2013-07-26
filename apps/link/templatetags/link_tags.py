# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template


register = template.Library()


@register.simple_tag
def link_draw(link):
    html = """
        <a href="%(url)s"> <img src="%(image)s" alt="%(label)s"> %(label)s </a>
    """
    args = { 
        "label" : link.get_label(), 
        "image" : link.get_image(), 
        "url" : link.get_url() 
    }
    return html % args


