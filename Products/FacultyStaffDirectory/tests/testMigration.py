# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone, PACKAGE_HOME
import os
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.CMFCore.utils import getToolByName

class testMigration(testPlone):
    """Test-cases for FacultyStaffDirectory migration."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Import the 1.0.1 zexp
        filename = os.path.join(PACKAGE_HOME, 'input', 'FSD1dot0dot1example.zexp')
        self.portal._importObjectFromFile(filename, verify=0)
        self.directory = self.portal['FSD1dot0dot1example']
        
    def test1dot0to2dot0Migration(self):
        try:
            manage_addExternalMethod(self.portal, 'migrationScript', 'migrate', 'FacultyStaffDirectory.migrate1dot0to2dot0', 'migrate')
            output = self.portal.migrationScript()
            cat = getToolByName(self.portal, 'portal_catalog') 
            
            # Make sure all of the portal_types are correct
            oldPortalTypes = ["FacultyStaffDirectory", "Classification", "Person", "Course", "CommitteesFolder", "Committee", "Specialty", "SpecialtiesFolder", "PersonGrouping", "Department", "CommitteeMembership", "SpecialtyInformation", "DepartmentalMembership"]
            for type in oldPortalTypes:
                results = cat(portal_type=type)
                self.failIf(results)
                # Let's check the meta_type while we're at it.
                results = cat(meta_type=type)
                self.failIf(results)
            
            # Make sure classifications are properly hooked-up
            self.failIf('aaa111' not in [p.id for p in self.directory.faculty.getPeople()])

            # Make sure Kupu customizations are updated
            kupu = getToolByName(self, 'kupu_library_tool')
            resourceList = list(kupu.getPortalTypesForResourceType('linkable'))
            self.failIf('Person' in resourceList)
            self.failIf('FSDPerson' not in resourceList)
            
        except ImportError, detail:
            # "contentmigration" product was not found, no migration performed.
            print detail
            
    def testMigrationImport(self):
        self.failUnless(self.directory)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMigration))
    return suite
