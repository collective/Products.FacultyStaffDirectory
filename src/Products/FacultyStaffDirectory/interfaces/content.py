# -*- coding: utf-8 -*-
"""Interfaces for content types (and a tool)"""
# TODO: Stick methods or at least docstrings describing the contracts on these!

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface
from zc.relationship.interfaces import IRelationship

class IPersonGrouping(Interface):
    """A grouping of person objects"""

    def getPeople():
        """Return a list of people."""

    def getSortedPeople():
        """Return a sorted list of people."""

class ICourse(Interface):
    """A course"""

class IFacultyStaffDirectory(Interface):
    """A FacultyStaffDirectory."""
                               
class IFacultyStaffDirectoryAddable(Interface):
    """A content type to be set as an addable_type within a FacultyStaffDirectory."""

class IPerson(Interface):
    """A person"""

class IFacultyStaffDirectoryTool(Interface):
    """The FacultyStaffDirectory tool"""

class IAssociationContent(Interface):
    """Marker interface for AssociationContent objects"""

class IPersonToPersonGroupingRelationship(IRelationship):
    """Marker interface for a Person->PersonGrouping relationship."""
    
class IPersonToPersonRelationship(IRelationship):
    """Marker interface for a Person->Person relationship."""