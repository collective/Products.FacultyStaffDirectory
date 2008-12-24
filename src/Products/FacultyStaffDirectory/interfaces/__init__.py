# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

# Subpackages
import classification
import committee
import committeemembership
import course
import department
import departmentalmembership
import facultystaffdirectory
import person
import specialtiesfolder
import specialty
import specialtyinformation
import tree

from zope.interface import Interface

from Products.FacultyStaffDirectory.interfaces.configuration import IConfiguration, IGeneralConfiguration, IMembershipConfiguration
from Products.FacultyStaffDirectory.interfaces.events import IMembraneIntegrationModifiedEvent

class ISiteMarker(Interface):
    """Marker interface applied to Plone sites in which FSD is installed"""
