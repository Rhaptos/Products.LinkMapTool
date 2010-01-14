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


from Products.RhaptosTest import config
import Products.LinkMapTool
import Products.RhaptosRepository
config.products_to_load_zcml = [
    ('configure.zcml', Products.LinkMapTool),
    ('configure.zcml', Products.RhaptosRepository),
]
config.products_to_install = [
    'Archetypes', 'CMFCore', 'CMFDefault', 'LinkMapTool', 'MailHost',
    'MimetypesRegistry', 'PortalTransforms', 'RhaptosCollection',
    'RhaptosHitCountTool', 'RhaptosModuleEditor', 'RhaptosRepository',
    'ZAnnot', 'ZCTextIndex',
]
config.extension_profiles = [
    'Products.LinkMapTool:default', 'Products.RhaptosCollection:default',
    'Products.RhaptosRepository:default',
]

from Products.CMFCore.utils import getToolByName
from Products.LinkMapTool.LinkMapTool import LinkMapTool
from Products.LinkMapTool.interfaces.portal_linkmap import portal_linkmap as ILinkMapTool
from Products.RhaptosTest import base


class TestLinkMapTool(base.RhaptosTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        # FIXME:  This following chunk of code was copied and adapted from
        # RhaptosRepository's setuphandlers.  We shouldn't have to do this
        # stuff manually.  setuphandlers should get run when we install the
        # RhaptosRepository product.
        product = self.portal.manage_addProduct['RhaptosRepository']
        product.manage_addRepository('content')
        self.repo = self.portal.content

        self.link_map_tool = getToolByName(self.portal, 'portal_linkmap')

    def beforeTearDown(self):
        pass

    def test_interface(self):
        # Make sure that link map tool implements the expected interface.
        self.failUnless(ILinkMapTool.isImplementedBy(self.link_map_tool))

    def test_link_map_tool(self):
        # Make sure that there are no links with the source
        # 'http://www.google.com/'.
        links = self.link_map_tool.searchLinks(source='http://www.google.com/')
        self.assertEqual(len(links), 0)

        # Add a link with the source 'http://www.google.com/'.
        source = 'http://www.google.com/'
        target = 'http://grab-it.appspot.com/'
        title = 'grab-it - social bookmarking'
        category = 'web 2.0'
        strength = 100
        self.link_map_tool.addLink(source, target, title, category, strength)

        # Make sure that there's a link with the source
        # 'http://www.google.com/'.
        links = self.link_map_tool.searchLinks(source='http://www.google.com/')
        self.assertEqual(len(links), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLinkMapTool))
    return suite
