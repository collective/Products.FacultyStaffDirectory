# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.config import PROJECTNAME


__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'


def install(self, reinstall=False):
    """ External Method to install FacultyStaffDirectory """

    def importProfiles(self, importContexts):
        """Import all steps from the GenericSetup profiles listen in `importContexts`."""
        setupTool = getToolByName(self, 'portal_setup')
        for eachContext in importContexts:
            setupTool.runAllImportStepsFromProfile(eachContext)

    profilesToImport = ('profile-Products.FacultyStaffDirectory:default',)
    importProfiles(self, profilesToImport)

def uninstall(self, reinstall=False):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:uninstall')

