# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Specialty
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase

class testSpecialty(FacultyStaffDirectoryTestCase):
    """Test-cases for class(es) Specialty."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.sf = self.directory.getSpecialtiesFolder()
        self.sf.invokeFactory(type_name="FSDSpecialty", id="test-specialty")
        self.specialty = self.sf['test-specialty']

    def testAddPersonToSpecialty(self):
        #Assign a person to a specialty
        self.specialty.addReference(self.person, relationship='SpecialtyInformation')
        self.failUnless(self.person in self.specialty.getPeople())
        
    def testAddSubSpecialty(self):
        #Make sure we can add a specialty within a specialty
        self.specialty.invokeFactory(type_name="FSDSpecialty", id="test-subspecialty")
        self.failUnless('test-subspecialty' in self.specialty.contentIds())
    
    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDSpecialty'].Title() != "AT Content Type")
        self.failUnless(self.portal.portal_types['FSDSpecialtyInformation'].Title() != "AT Content Type")

    def testObjectReorder(self):
        """ Make sure we can reorder objects within this folderish content type. """
        self.specialty.invokeFactory(type_name="FSDSpecialty", id="o1") 
        self.specialty.invokeFactory(type_name="FSDSpecialty", id="o2") 
        self.specialty.invokeFactory(type_name="FSDSpecialty", id="o3") 
        self.specialty.moveObjectsByDelta(['o3'], -100)
        self.failUnless(self.specialty.getObjectPosition('o3') == 0, "FSDSpecialty Subobject 'o3' should be at position 0.")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSpecialty))
    return suite
