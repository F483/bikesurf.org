# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE.TXT file)


"""
Tests links to external sites
"""


from django.test import TestCase
from apps.link import control as link_control

class ValidSiteLinks(TestCase):
    def test_couchsurfing_com_links(self):
        """
        Tests that .com urls are accepted
        """
        self.assertEqual(True, link_control.valid_profile_format("https://couchsurfing.com/people/deivid_rodriguez", "COUCHSURFING"))

