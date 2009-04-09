# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Committee
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase

class testCommittee(FacultyStaffDirectoryTestCase):
    """Test-cases for class(es) Committee."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")
        cid = self.directory['committees'].invokeFactory('FSDCommittee',id='mycommittee',title="My Committee")
        self.committee = self.directory['committees'].mycommittee
        
    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDCommittee'].Title() != "AT Content Type")
        self.failUnless(self.portal.portal_types['FSDCommitteeMembership'].Title() != "AT Content Type")

    def testObjectReorder(self):
        """ Make sure we can reorder objects within this folderish content type. """
        self.committee.invokeFactory(type_name="Document", id="o1") 
        self.committee.invokeFactory(type_name="Document", id="o2") 
        self.committee.invokeFactory(type_name="Document", id="o3") 
        self.committee.moveObjectsByDelta(['o3'], -100)
        self.failUnless(self.committee.getObjectPosition('o3') == 0, "Document subobject 'o3' should be at position 0.")
        
    def testCommitteeIsNestable(self):
        """ Make sure that classifications can be added inside classifications
        """
        try:
            self.committee.invokeFactory('FSDCommittee', id='nested-committee', title='Nested Committee')
        except ValueError:
            self.fail('Cannot add a committee inside a committee')
        
    def testValidateId(self):
        """Test that the validate_id validator works properly
        """
        from Products.CMFCore.utils import getToolByName
        
        # setup some content to test against
        self.directory['committees'].invokeFactory('FSDCommittee','com1')
        pg = getToolByName(self.directory,'portal_groups')
        pg.addGroup('group1');
        
        #allow unused id
        self.failUnless(self.committee.validate_id('foo')==None,
                        "failed to validate_id 'foo': %s" % self.committee.validate_id('foo'))
        # allow current object id
        self.failUnless(self.committee.validate_id(self.committee.getId())==None,
                        "Failed to validate current id of committee object: %s" % self.committee.getId())
        # deny id of other object in site
        self.failUnless('com1' in self.committee.validate_id('com1'),
                        "Allowed id 'com1', even though there is an object with that id in the committees folder: %s" % self.committee.validate_id('com1'))
        # deny id of other group for site
        self.failUnless('group1' in self.committee.validate_id('group1'),
                        "Allowed id 'group1', even though there is a group with that id in the portal: %s" % self.committee.validate_id('group1'))
        
    ## end test membrane stuff
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCommittee))
    return suite
