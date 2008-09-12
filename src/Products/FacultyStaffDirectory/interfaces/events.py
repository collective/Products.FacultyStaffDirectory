# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface, Attribute


class ICommitteeModifiedEvent(Interface):
    """An event fired when a Committee object is saved."""
    context = Attribute("The content object that was saved.")

class IFacultyStaffDirectoryModifiedEvent(Interface):
    """An event fired when an FacultyStaffDirectory object is saved."""
    context = Attribute("The content object that was saved.")
                               
class IPersonModifiedEvent(Interface):
    """An event fired when a person object is saved"""
    context = Attribute("The content object that was saved.")

class IFacultyStaffDirectoryToolModifiedEvent(Interface):
    """An event fired when the facultystaffdirectory_tool is saved."""
