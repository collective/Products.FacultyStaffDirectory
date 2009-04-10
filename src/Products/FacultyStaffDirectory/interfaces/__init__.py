# -*- coding: utf-8 -*-
# Import interfaces from here, not from the submodules, which are subject to reorganization.

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface
from Products.FacultyStaffDirectory.interfaces.content import IPersonGrouping, IClassification, ICourse, IFacultyStaffDirectory, IFacultyStaffDirectoryAddable, IPerson, IFacultyStaffDirectoryTool
from Products.FacultyStaffDirectory.interfaces.browser import IPersonViewletManager, IPersonOfficeAddressViewletManager, IPersonView, IPersonGroupingViewletManager, IPersonGroupingContainerViewletManager, IPersonGroupingView, IClassificationViewletManager, IListingFormat, ITabularListingFormat, IGalleryListingFormat
from Products.FacultyStaffDirectory.interfaces.configuration import IConfiguration, IGeneralConfiguration, IMembershipConfiguration
from Products.FacultyStaffDirectory.interfaces.events import IMembraneIntegrationModifiedEvent, IPersonModifiedEvent
from Products.FacultyStaffDirectory.interfaces.tree import ITree

class ISiteMarker(Interface):
    """Marker interface applied to Plone sites in which FSD is installed"""
