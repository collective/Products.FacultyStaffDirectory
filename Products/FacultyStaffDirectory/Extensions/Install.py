# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.config import PROJECTNAME


__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'


def install(self, reinstall=False):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:default')

def uninstall(self, reinstall=False):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:uninstall')

