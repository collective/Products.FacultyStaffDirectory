# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface, Attribute

class ICommittee(Interface):
    """a committee
    """
    
class ICommitteeModifiedEvent(Interface):
    """An event fired when a Committee object is saved.
    """
    
    context = Attribute("The content object that was saved.")



