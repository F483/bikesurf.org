# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.dispatch import Signal


team_created = Signal(providing_args=["team", "creator"])
join_request_created = Signal(providing_args=["join_request"])
join_request_processed = Signal(providing_args=["join_request"])
remove_request_created = Signal(providing_args=["remove_request"])
remove_request_processed = Signal(providing_args=["remove_request"]) # TODO


