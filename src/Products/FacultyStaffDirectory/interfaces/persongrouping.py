# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IPersonGrouping(Interface):
    """A grouping of person objects
    """

    def getSortedPeople():
        """Return a list of sorted people
        """
