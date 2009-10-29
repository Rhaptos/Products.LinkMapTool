#------------------------------------------------------------------------------#
#   test_link_map_tool.py                                                      #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Unit tests.
$Id: $
"""


import Products.LinkMapTool

from Products.LinkMapTool.LinkMapTool import LinkMapTool
from Products.RhaptosTest.base import RhaptosTestCase


class TestLinkMapTool(RhaptosTestCase):

    products_to_load_zcml = [('configure.zcml', Products.LinkMapTool),]

    def setUp(self):
        RhaptosTestCase.setUp(self)
        self.link_map_tool = LinkMapTool()

    def test_link_map_tool(self):
        links = self.link_map_tool.searchLinks()
        self.assertEqual(len(links), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLinkMapTool))
    return suite
