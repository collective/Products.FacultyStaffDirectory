# -*- coding: utf-8 -*-
"""Interfaces for content types (and a tool)"""
# TODO: Stick methods or at least docstrings describing the contracts on these!

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IPersonGrouping(Interface):
    """A grouping of person objects"""

    def getPeople():
        """Return a list of people."""

    def getSortedPeople():
        """Return a sorted list of people."""

class IClassification(IPersonGrouping):
    """A classification"""

class ICommittee(IPersonGrouping):
    """A committee"""
    
class ICommitteeMembership(Interface):
    """A committee membership"""

class ICommitteesFolder(Interface):
    """A committees folder"""

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
