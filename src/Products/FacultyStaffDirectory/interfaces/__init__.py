# -*- coding: utf-8 -*-
# Import interfaces from here, not from the submodules, which are subject to reorganization.

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from content import IPersonGrouping, IClassification, IDepartment, ISpecialty, ICommittee, ICommitteeMembership, ICommitteesFolder, ICourse, IDepartmentalMembership, IFacultyStaffDirectory, IFacultyStaffDirectoryAddable, IPerson, ISpecialtiesFolder, ISpecialtyInformation, IFacultyStaffDirectoryTool
from events import ICommitteeModifiedEvent, IFacultyStaffDirectoryModifiedEvent, IPersonModifiedEvent, IFacultyStaffDirectoryToolModifiedEvent
from membership import IGroupingProvidingMembership
