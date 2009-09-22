"""
LinkMapTool.py - Manages links on objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import os
import urlparse
import zLOG
import AccessControl
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.CMFCorePermissions import View, ManagePortal
from interfaces.portal_linkmap import portal_linkmap as ILinkMapTool
from Products.ZCatalog.ZCatalog import ZCatalog

#manage_addCNXMLFileForm = PageTemplateFile('zpt/manage_addCNXMLFileForm',
#                                           globals(),
#                                           __name__='manage_addCNXMLFileForm')

def manage_addLink(self, id, REQUEST=None):
    """Add a new Link object."""

    id=str(id)
    self=self.this()

    self._setObject(id, ExtendedLink(id))

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')


class ExtendedLink(SimpleItem):
    """An extended Link"""

    meta_type = "Extended Link"

    def __init__(self,
                 id,
                 source='',
                 target='',
                 category='',
                 strength=0,
                 title='',
                 description=''):
        """ExtendedLink constructor"""

        self.id = id
        self.edit(source, target, title, category, strength)
        self.description = description

    def edit(self, source, target='', title='', category='', strength=0):
        """
            Edit the Link
        """
        tokens = urlparse.urlparse( target, 'http' )
        if tokens[0] == 'http':
            if tokens[1]:
                # We have a nethost. All is well.
                url = urlparse.urlunparse(tokens)
            elif tokens[2:] == ('', '', '', ''):
                # Empty URL
                url = ''
            else:
                # Relative URL, keep it that way, without http:
                tokens = ('', '') + tokens[2:]
                url = urlparse.urlunparse(tokens)
        else:
            # Other scheme, keep original
            url = urlparse.urlunparse(tokens)
        self.target = url
        self.source = source
        self.category = category
        self.strength = int(strength)
        self.title = title

# BW Compatibility
RisaLink = ExtendedLink

class LinkMapTool(UniqueObject, BTreeFolder2):

    __implements__ = (ILinkMapTool)

    id = 'portal_linkmap'
    meta_type = 'LinkMap Tool'
    security = AccessControl.ClassSecurityInfo()

    manage_options=(( {'label':'Overview', 'action':'manage_overview'},
                      { 'label' : 'Catalog', 'action' : 'manage_catalog'},
                      ) + BTreeFolder2.manage_options
                    )

    ##   ZMI methods
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = PageTemplateFile('zpt/explainLinkMapTool', globals() )

    security.declareProtected(ManagePortal, 'manage_catalog')
    def manage_catalog(self, REQUEST=None):
        """Access to the ZCatalog"""
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.catalog.absolute_url()+'/manage_catalogView')


    def __init__(self, *args, **kw):
        BTreeFolder2.__init__(self, *args, **kw)
        self._create_catalog()
        self._linkrange = (1,3)  # currently unused; just a marker

    security.declarePrivate("_create_catalog")
    def _create_catalog(self):
        """Creates the ZCatalog instance for searching links"""
#        self.catalog = ZCatalog('catalog').__of__(self)
        self.catalog = ZCatalog('catalog')
        
        self.catalog.addIndex('source', 'FieldIndex')
        self.catalog.addIndex('strength', 'FieldIndex')

        self.catalog.addColumn('target')
        self.catalog.addColumn('category')
        self.catalog.addColumn('strength')
        self.catalog.addColumn('title')

        self._p_changed=1


    security.declareProtected('LinkMap: Add Link', 'addLink')
    def addLink(self, source, target, title, category, strength, context=None):
        """Create a link"""
        
        id = self.generateId()
        self._setObject(id, ExtendedLink(id))
        ob = getattr(self, id)
        ob.edit(source, target, title, category, strength)

        self.catalog.catalog_object(ob)

    security.declarePublic('searchLinks')
    def searchLinks(self, source=None, context=None):
        """Return all links for a particular source and context"""
        # FIXME: do we have to worry about 'latest' translation?
        results = self.catalog(source=source, sort_on='strength', sort_order='descending')
        
        return results

    def deleteLinks(self,objectId,version=None):
        """Delete all links for which the objectId is either source or target"""
	# This code assumes a ZRepository instance at /content
        myhost = urlparse.urlparse(self.REQUEST.SERVER_URL)[1]
	mypath = '/'.join(filter(None,['/content',objectId,version]))
	mylinks = []
	
	# FIXME: once a better storage and search interface exists, we can use that
	for link in self.objectValues('Extended Link'):
	    #Check source
	    tokens = urlparse.urlparse(link.source)
	    if (tokens[1] or myhost) == myhost and tokens[2].startswith(mypath): 
	        mylinks.append(link.id)
	    else:
	    #Check target
	        tokens = urlparse.urlparse(link.target)
	        if (tokens[1] or myhost) == myhost and tokens[2].startswith(mypath): 
	            mylinks.append(link.id)

	# Blow'em away!
        self.manage_delObjects(mylinks)

	
    security.setPermissionDefault('LinkMap: Add Link', ('Manager', 'Owner',))

InitializeClass(ExtendedLink)
InitializeClass(LinkMapTool)


