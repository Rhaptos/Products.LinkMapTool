"""
strength.py - utility functions for strengths

Author: J Cameron Cooper (jccooper@rice.edu, jccooper@gmail.com)
Copyright (C) 2009 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

map5to3 = {
           1:1, 2:1,
           3:2, 4:2,
           5:3
           }
def upgrade5to3(old):
    """Change a 5-level strength value to a 3-level strength value.
    Give int 1-5.
    Return int 1-3, based on 'old' input.
    KeyError if input is bad.
    """
    return map5to3[int(old)]