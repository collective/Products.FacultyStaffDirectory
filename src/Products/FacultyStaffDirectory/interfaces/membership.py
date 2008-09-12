# -*- coding: utf-8 -*-
"""Interfaces involved with user and group integration"""

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

from Products.FacultyStaffDirectory.interfaces import IPersonGrouping

class IGroupingProvidingMembership(IPersonGrouping):
    """A grouping of person objects that provides group membership to those in it"""
