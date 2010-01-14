"""
Initialize LinkMapTool Product

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import sys
from Products.CMFCore import utils
import LinkMapTool


this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( LinkMapTool.LinkMapTool,)

def initialize(context):
    utils.ToolInit('LinkMap Tool',
                    tools = tools,
                    icon='tool.gif' 
                    ).initialize( context )

    context.registerClass(LinkMapTool.ExtendedLink,
                          constructors=(LinkMapTool.manage_addLink,
                                        LinkMapTool.manage_addLink),
                          )
