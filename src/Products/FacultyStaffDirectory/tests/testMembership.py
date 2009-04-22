# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for membership functionality
#
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase

from Products.membrane.interfaces import IGroup

class testMembership(FacultyStaffDirectoryTestCase):
    """Tests for membership functionality in FSD classes"""
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.wf = getToolByName(self.portal, 'portal_workflow')
        self.directory = self.getPopulatedDirectory()
        # setup some people
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")
        self.person3 = self.getPerson(id='ghi789', firstName="Testier", lastName="Persona")
        # setup some person groupings
        self.personGrouping = self.directory.getPersonGroupings()[0].getObject()
        self.personGrouping.invokeFactory(type_name="FSDPersonGrouping", id="academic-faculty", title="Academic Faculty")
        self.nested_grouping = self.personGrouping['academic-faculty']
        
    def testTypesAreGroups(self):
        """Verify that all membrane-able content types are functioning as groups"""
        for obj in [self.personGrouping, self.nested_grouping, self.directory]:
            self.failUnless(self.acl_users.getGroupById(obj.getId()),"unable to find group with id of this %s: %s" % (obj.portal_type ,obj.getId()))
        
    def testIGroupAdapts(self):
        """Verify that the IGroup interface successfully adapts our membrane content types"""
        for obj in [self.personGrouping, self.nested_grouping, self.directory]:
            try:
                IGroup(obj)
            except TypeError:
                self.fail('Unable to adapt %s object to IGroup' % obj.portal_type)
                
    def testGroupTitle(self):
        """Test the Title method of the IGroup adapter"""
        for obj in [self.personGrouping, self.nested_grouping, self.directory]:
            g = IGroup(obj)
            obj.setTitle('New Title')
            self.failUnlessEqual(g.Title(), 'New Title', "IGroup is returning the incorrect title for %s.  Expected %s, got %s" % (obj.portal_type, obj.Title(), g.Title()))
        
    def testGroupRoles(self):
        """Test the getGroupRoles method of the IGroup adapter"""
        # first test the persongrouping types, which should not support roles
        for obj in [self.personGrouping, self.nested_grouping]:
            g = IGroup(obj)
            # the IGroup adapter should never return roles for these types
            self.failIf(g.getRoles(), "%s should not provide roles" % obj.portal_type)
            try:
                # this should throw an error, because these content types should have no roles field
                aq_inner(obj).aq_explicit.setRoles(('Reviewer',))
                self.fail("%s should not have a roles field in its schema, but does" % obj.portal_type)
            except AttributeError:
                pass
                
        # now test the directory itself, which should
        g = IGroup(self.directory)
        #roles are set on the object, but only available when object is published
        self.directory.setRoles(('Reviewer',))
        # at first, object is 'visible', but not published, roles should be empty
        self.failIf('Reviewer' in g.getRoles(),"roles are active, but content unpublished\nRoles: %s\nReviewState: %s" % (g.getRoles(), self.wf.getInfoFor(self.directory,'review_state')))
        #publish object
        self.wf.doActionFor(self.directory,'publish')
        # now check again, role should be there
        self.failUnless('Reviewer' in g.getRoles(),"Roles not active, but content published\nRoles: %s\nReviewState: %s" % (g.getRoles(), self.wf.getInfoFor(self.directory,'review_state')))
        
    def testGroupID(self):
        """Test the getGroupId method of the IGroup adapter"""
        for obj in [self.personGrouping, self.nested_grouping, self.directory]:
            g = IGroup(obj)
            self.failUnlessEqual(g.getGroupId(), obj.getId(), "IGroup is returning the incorrect ID for %s.  Expected %s, got %s" % (obj.portal_type, obj.getId(), g.getGroupId()))
    
    def testGroupMembership(self):
        """Test the getGroupMembers method of the IGroup adapter"""
        # add people to outer groups
        for obj in [self.personGrouping]:
            obj.setPeople([self.person.UID(), self.person2.UID()])
        # add people to inner groups
        for obj in [self.nested_grouping]:
            obj.setPeople([self.person3.UID()])
        
        # check member list of outer objects
        for obj in [self.personGrouping]:
            g = IGroup(obj)
            mlist = list(g.getGroupMembers())
            mlist.sort()
            self.failUnlessEqual(mlist, ['abc123', 'def456', 'ghi789'], 'Incorrect member list for top-level %s: %s' % (obj.portal_type, mlist))
        
        # check member list of inner objects
        for obj in [self.nested_grouping]:
            g = IGroup(obj)
            mlist = list(g.getGroupMembers())
            mlist.sort()
            self.failUnlessEqual(mlist, ['ghi789',], 'Incorrect member list for top-level %s: %s' % (obj.portal_type, mlist))
            
        # check group membership for FSD itself
        g = IGroup(self.directory)
        mlist = list(g.getGroupMembers())
        mlist.sort()
        self.failUnlessEqual(mlist, ['abc123', 'def456', 'ghi789'], 'Incorrect member list for %s: %s' % (self.directory.portal_type, mlist))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMembership))
    return suite