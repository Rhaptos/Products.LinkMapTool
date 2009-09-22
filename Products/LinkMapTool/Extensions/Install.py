from Products.LinkMapTool.strengths import upgrade5to3

from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import string

import logging
logger = logging.getLogger('LinkMapTool.Install')
def log(msg, out=None):
    logger.info(msg)
    if out: print >> out, msg

def install(self):
    """Add the tool, upgrade if necessary. Upgrade requires run as Manager."""
    out = StringIO()
    log("Starting install of LinkMapTool", out)

    # Add the tool
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();

    try:
        lmtool = getToolByName(self, 'portal_linkmap')
        lmcat = lmtool.catalog
        log("Tool already exists: checking for upgrades...", out)
        if not getattr(lmtool, '_linkrange', None):
            log("...adding strength range attribute", out)
            lmtool._linkrange = (1,3)  # TODO: GLOBAL

            log("...migrating strength range attribute from 1-5 to 1-3", out)
            record = StringIO()
            alllinks = lmtool.objectValues()
            for l in alllinks:
                # record existing state
                ldict = {'source':l.source, 'target':l.target, 'title':l.title, 'strength':l.strength}
                record.write(str(ldict)+"\n")
                # update object attr
                l.strength = upgrade5to3(l.strength)
                # update catalog entries
                lmcat.catalog_object(l, update_metadata=1, idxs=['strength'])
            olddata = portal.invokeFactory(type_name="File", id="linkconv-linkmaptool",
                                           title="LinkMapTool old 5-level data, from upgrade", file=record)
            olddata = portal[olddata]
            log("Migrated %s links in portal_linkmap" % len(alllinks), out)
            log("5-level data recorded in File at %s" % olddata.absolute_url(), out)
    except AttributeError:
        log("Adding LinkMap Tool", out)
        portal.manage_addProduct['LinkMapTool'].manage_addTool('LinkMap Tool', None)

    log("Successfully installed LinkMapTool", out)
    return out.getvalue()
