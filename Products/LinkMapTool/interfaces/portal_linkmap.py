# Copyright (c) 2003 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks

""" File system import interface"""

from zope.interface import Attribute
from zope.interface import Interface

class portal_linkmap(Interface):
    """Provides ability to store contentlinks with properties"""

    id = Attribute('id','Must be set to "portal_linkmap"')

    def addLink(source, target, title, category, strength, context=None):
        """Create a link"""

    def searchLinks(source=None, context=None):
        """Search for links"""
