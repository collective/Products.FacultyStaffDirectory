# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface, Attribute

class IMembraneIntegrationModifiedEvent(Interface):
    """Event fired when membrane integration is enabled or disabled for one or more FSD types"""
