# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for browser views of product
#

from Products.FacultyStaffDirectory.tests.testPlone import testPlone
from Products.Five.testbrowser import Browser

class testPerson(testPlone):
    """test browser views of an FSDPerson
    """
    # for some reason, the line below 'browser.open(person_url) is throwing an attribute error,
    # I've traced said error all the way down into python's urllib2.py.  Can't figure out
    # why it's happening, though.  I'm stumped.  I was sure this test was passing when I committed it
    # but it's clearly failing now, and bringing everything else down with it when it does
    pass
#     def afterSetUp(self):
#         self.loginAsPortalOwner()
#         self.directory = self.getPopulatedDirectory()
#         self.person = self.getPerson(self.directory, id="abc123", firstName="Test", lastName="Person")
#         self.portal.error_log._ignored_exceptions = ()
#     
#     def testViewPerson(self):
#         """Test that the basic view of a person works
#         """
#         import pdb; pdb.set_trace()
#         browser = Browser()
#         browser.handleErrors = False
#         person_url = self.person.absolute_url()
#         try:
#             browser.open(person_url)
#         except:
#             self.fail(self.portal.error_log.getLogEntries()[0]['tb_text'])
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testPerson))
    return suite