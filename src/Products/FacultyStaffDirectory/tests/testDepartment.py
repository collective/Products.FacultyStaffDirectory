# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Committee
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase
from Products.CMFCore.utils import getToolByName

class testDepartment(FacultyStaffDirectoryTestCase):
    """Test-cases for class(es) Department."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.directory.invokeFactory(type_name="FSDDepartment", id="test-department-inside", title="Inside Department") 
        self.portal.invokeFactory(type_name="FSDDepartment", id="test-department-outside", title="Outside Department") 
        self.inDept = self.directory['test-department-inside']
        self.outDept = self.portal['test-department-outside']
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDDepartment'].Title() != "AT Content Type")
        self.failUnless(self.portal.portal_types['FSDDepartmentalMembership'].Title() != "AT Content Type")

    def testCreateDepartment(self): 
        # Make sure Departments can be added within FSDs
        self.failUnless('test-department-inside' in self.directory.contentIds())
        
    def testDepartmentIsNestable(self):
        """ Make sure that classifications can be added inside classifications
        """
        try:
            self.inDept.invokeFactory('FSDDepartment', id='nested-dept', title='Nested Department')
        except ValueError:
            self.fail('Cannot add a department inside a department')
        
    def testValidateId(self):
        """Test that the validate_id validator works properly
        """
        from Products.CMFCore.utils import getToolByName
        
        # setup some content to test against
        self.directory.invokeFactory('Document','doc1')
        pg = getToolByName(self.directory,'portal_groups')
        pg.addGroup('group1');
        
        #allow unused id
        self.failUnless(self.inDept.validate_id('foo')==None,"failed to validate_id 'foo': %s" % self.inDept.validate_id('foo'))
        # allow current object id
        self.failUnless(self.inDept.validate_id(self.inDept.getId())==None,"Failed to validate current id of classification object: %s" % self.inDept.id)
        # deny id of other object in site
        self.failUnless('doc1' in self.inDept.validate_id('doc1'),"Allowed id 'doc1', even though there is an object with that id in the portal: %s" % self.inDept.validate_id('doc1'))
        # deny id of other group for site
        self.failUnless('group1' in self.inDept.validate_id('group1'),"Allowed id 'doc1', even though there is a group with that id in the portal: %s" % self.inDept.validate_id('group1'))

    def testGroupTitle(self):
        """ Verify that group titles are being set properly.
        """
        acl = getToolByName(self.portal, 'acl_users')
        ind = acl.getGroupById('test-department-inside')
        self.failUnless(ind.Title() == 'Inside Department', "KnownFailure: Unexpected value for Title for group 'faculty'. Got '%s', expected 'Inside Department'." % ind.Title())
        

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testDepartment))
    return suite
