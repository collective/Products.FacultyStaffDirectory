# -*- coding: utf-8 -*-
# Import interfaces from here, not from the submodules, which are subject to reorganization.

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from Products.FacultyStaffDirectory.interfaces.content import IPersonGrouping, IClassification, IDepartment, ISpecialty, ICommittee, ICommitteeMembership, ICommitteesFolder, ICourse, IDepartmentalMembership, IFacultyStaffDirectory, IFacultyStaffDirectoryAddable, IPerson, ISpecialtiesFolder, ISpecialtyInformation, IFacultyStaffDirectoryTool
from Products.FacultyStaffDirectory.interfaces.events import ICommitteeModifiedEvent, IFacultyStaffDirectoryModifiedEvent, IPersonModifiedEvent, IFacultyStaffDirectoryToolModifiedEvent
from Products.FacultyStaffDirectory.interfaces.membership import IGroupingProvidingMembership
from Products.FacultyStaffDirectory.interfaces.browser import IPersonViewletManager, IPersonView, IPersonGroupingViewletManager, IPersonGroupingContainerViewletManager, IPersonGroupingView, ISpecialtyViewletManager, IClassificationViewletManager, ICommitteeViewletManager, IDepartmentViewletManager, ITabularListing, IGalleryListing
