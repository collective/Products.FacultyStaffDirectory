# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IPersonGrouping(Interface):
    """A grouping of person objects"""

    def getPeople():
        """Return a list of people."""

    def getSortedPeople():
        """Return a sorted list of people."""
