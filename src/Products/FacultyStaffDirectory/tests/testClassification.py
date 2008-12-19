# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Classification
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase
from Products.CMFCore.utils import getToolByName

class testClassification(FacultyStaffDirectoryTestCase):
    """Test-cases for class(es) Classification."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")
        self.classification = self.directory.getClassifications()[0].getObject()

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile 
        """
        self.failUnless(self.portal.portal_types['FSDClassification'].Title() != "AT Content Type")
        
    def testClassificationIsNestable(self):
        """ Make sure that classifications can be added inside classifications
        """
        try:
            self.classification.invokeFactory('FSDClassification', id='nested-classification', title='Nested Classification')
        except ValueError:
            self.fail('Cannot add a classification inside a classification')
        
    def testValidateId(self):
        """Test that the validate_id validator works properly
        """
        from Products.CMFCore.utils import getToolByName
        
        # setup some content to test against
        self.directory.invokeFactory('Document','doc1')
        pg = getToolByName(self.directory,'portal_groups')
        pg.addGroup('group1');
        
        #allow unused id
        self.failUnless(self.classification.validate_id('foo')==None,"failed to validate_id 'foo': %s" % self.classification.validate_id('foo'))
        # allow current object id
        self.failUnless(self.classification.validate_id(self.classification.getId())==None,"Failed to validate current id of classification object: %s" % self.classification.id)
        # deny id of other object in site
        self.failUnless('doc1' in self.classification.validate_id('doc1'),"Allowed id 'doc1', even though there is an object with that id in the portal: %s" % self.classification.validate_id('doc1'))
        # deny id of other group for site
        self.failUnless('group1' in self.classification.validate_id('group1'),"Allowed id 'doc1', even though there is a group with that id in the portal: %s" % self.classification.validate_id('group1'))

    def testGroupTitle(self):
        """ Verify that group titles are being set properly.
        """
        acl = getToolByName(self.portal, 'acl_users')
        fac = acl.getGroupById('faculty')
        self.failUnless(fac.Title() == 'Faculty', "KnownFailure: Unexpected value for Title for group 'faculty'. Got '%s', expected 'Faculty'." % fac.Title())
        
    ## end membrane tests
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testClassification))
    return suite
