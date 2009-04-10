# -*- coding: utf-8 -*-
"""Test-cases for Faculty/Staff Directory utility"""

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.component import getUtility
from zope.schema import Choice
from zope.schema.interfaces import ConstraintNotSatisfied
from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

from Products.FacultyStaffDirectory.interfaces import IConfiguration
from Products.FacultyStaffDirectory.config import MEMBRANE_ABLE_TYPES_CHOICES, MEMBRANE_ABLE_TYPES
from Products.FacultyStaffDirectory.tests.base import FacultyStaffDirectoryTestCase

class testFacultyStaffDirectoryUtility(FacultyStaffDirectoryTestCase):
    """Test cases for FacultyStaffDirectory configuration utility."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.fsd_utility = self.portal.getSiteManager().getUtility(IConfiguration)
        # set up an additional, non-fsd user for testing folder and profile methods
        self.portal.acl_users._doAddUser('user1','secret',['Member'],[])
        self.mt = getToolByName(self.person,'portal_membership')
        
    def testUseInternalPasswordControlsAuth(self):
        from Products.membrane.interfaces import IUserAuthentication
        
        u = IUserAuthentication(self.person)
        self.person.setPassword("chewy1")
        if self.fsd_utility.useInternalPassword:
            self.failUnless(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "useInternalPassword appears to be broken, failed to verify correct login and password: %s" % self.fsd_utility.useInternalPassword)
            self.fsd_utility.useInternalPassword = False
            self.failIf(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "useInternalPassword not toggled.  verification still allowed: %s" % self.fsd_utility.useInternalPassword)
        else:
            self.failIf(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "verification allowed, but shouldn't have been: %s" % self.fsd_utility.useInternalPassword)
            self.fsd_utility.useInternalPassword = True
            self.failUnless(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "useInternalPassword not toggled.  verification still disallowed: %s" % self.fsd_utility.useInternalPassword)
            
    def testIdRegexDefault(self):
        """Check to make sure the idRegex field is defaulting to the value set in portal_registration"""
        # get the value from portal_registration
        pr = getToolByName(self.portal, 'portal_registration')
        regPattern = pr.getIDPattern() or pr.getDefaultIDPattern()
        self.failUnlessEqual(self.fsd_utility.idRegex, unicode(regPattern))
        
    def testIdRegexChecking(self):
        """Make sure the id regex validation is working."""
        self.fsd_utility.idRegex = u'[A-Z]'
        self.fsd_utility.idRegexErrorMessage = u'Not even close.'
        self.failUnlessEqual(self.person.validate_id('123456'), u'Not even close.')        
        self.failIf(self.person.validate_id('ABC'))
        
    def testRegexValidation(self):
        """Make sure the value entered is a valid regular expression."""
        old_regex = self.fsd_utility.phoneNumberRegex
        try:
            try:
                self.fsd_utility.phoneNumberRegex = u']['
            except ConstraintNotSatisfied:
                pass
            else:
                self.fail(msg="Regular expression field validator let an invalid regex through.")
        finally:
            self.fsd_utility.phoneNumberRegex = old_regex
    
    def testGetDirectoryRoot(self):
        """Make sure this returns the containing FSD."""
        self.failUnlessEqual(self.person.getDirectoryRoot(), self.directory)
        
    def testFsdMyFolder(self):
        """fsdMyFolder method should return the appropriate url for non-fsd users or 
        for fsd users"""
        self.login(self.person.id)
        # logged in as an fsd user, the substring <directory_id/user_id> should be in the  return value for the function
        self.failUnless(self.fsd_utility.fsdMyFolder().find(self.directory.id + '/' + self.person.id), "bad url returned for %s: %s" % (self.person.id, self.fsd_utility.fsdMyFolder()))
        
        self.login('user1')
        # set up a memberarea
        if (not self.mt.getMemberareaCreationFlag()):
            self.mt.setMemberareaCreationFlag()
        self.mt.createMemberArea()
        try:
            self.failUnless(self.fsd_utility.fsdMyFolder().find(self.mt.getMembersFolder().id + '/user1'), "bad url returned for user1: %s" % self.fsd_utility.fsdMyFolder())
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")
            
    def testFsdMemberProfile(self):
        """fsdMemberProfile should return the location of the editor for member profile information.
        
        This will change depending on whether the member is an fsd person or an acl_users member.
        
        """
        self.login(self.person.id)
        # logged in as an fsd user, the substring <directory_id/user_id/edit> should be in the return value for the function
        self.failUnless(self.fsd_utility.fsdMemberProfile().find(self.directory.id + '/' + self.person.id), "bad url returned for %s: %s" % (self.person.id, self.fsd_utility.fsdMemberProfile()))
        
        # now as an acl_users user
        self.login('user1')
        try:
            self.failUnless(self.fsd_utility.fsdMemberProfile().find('/personalize_form'), "bad url returned for user1: %s" % self.fsd_utility.fsdMyFolder())
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")
            
    def testFsdShowMyFolder(self):
        """fsdShowMyFolder tries to intelligently decide whether to show the 'my folder' action
        button or not.  It tests to see if a member is an fsd person, and acts accordingly"""
        self.login(self.person.id)
        # logged in as an fsd user, the method should always return true
        self.failUnless(self.fsd_utility.fsdShowMyFolder(), "fsdShowMyFolder returning false for fsd user")
        
        # now as acl_users user
        self.login('user1')
        try:
            if (self.mt.getMemberareaCreationFlag() and (self.mt.getHomeFolder() is not None)):
                self.failUnless(self.fsd_utility.fsdShowMyFolder(), "should be showing my folder for acl_users, but we aren't")
            else:
                self.failIf(self.fsd_utility.fsdShowMyFolder(), "should not be showing my folder for acl_users, but we are")
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")

    def testMembraneTypeDeactivation(self):
        """Test that the fsd_utility's at_post_edit_script calls the modifyMembraneTypes event and
        that event correctly deals with membrane activation/deactivation."""
        # Be sure that FSDPerson is still a membrane provider, or the test will be invalid
        self.failUnless('FSDPerson' in MEMBRANE_ABLE_TYPES, "test invalid, FSDPerson is not listed as membrane-able")

        mbt = getToolByName(self.person, MEMBRANE_TOOL)
        uf = getToolByName(self.person, 'acl_users')
        mtypes = mbt.listMembraneTypes()

        # FSDPerson should be membrane-active at setup
        self.failUnless('FSDPerson' in self.fsd_utility.enableMembraneTypes and 'FSDPerson' in mtypes, "FSDPerson should be in both lists: %s, %s" % (self.fsd_utility.enableMembraneTypes, mtypes))
        self.failUnless(uf.getUserById('abc123'), "Person 'abc123' not registered as user via acl_users")
        
        # Now, let's edit the configuration:
        self.fsd_utility.enableMembraneTypes = MEMBRANE_ABLE_TYPES - set(('FSDPerson',))
        
        # FSDPerson should not be membrane-active
        mtypes = mbt.listMembraneTypes()
        self.failIf('FSDPerson' in self.fsd_utility.enableMembraneTypes or 'FSDPerson' in mtypes, "FSDPerson should not be in either list: %s, %s" % (self.fsd_utility.enableMembraneTypes, mtypes))
        self.failIf(uf.getUserById('abc123'), "Person 'abc123' active as a user after membrane de-activation")
        
        # Now, put everything back!
        self.fsd_utility.enableMembraneTypes = MEMBRANE_ABLE_TYPES
        
        # FSDPerson should be membrane-active again
        mtypes = mbt.listMembraneTypes()
        self.failUnless('FSDPerson' in self.fsd_utility.enableMembraneTypes and 'FSDPerson' in mtypes, "FSDPerson should be in both lists: %s, %s" % (self.fsd_utility.enableMembraneTypes, mtypes))
        self.failUnless(uf.getUserById('abc123'), "Person 'abc123' not active as a user after membrane re-activation")
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testFacultyStaffDirectoryUtility))
    return suite
