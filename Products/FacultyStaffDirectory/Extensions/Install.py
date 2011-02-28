# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'


def install(self, reinstall=False):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:default')

def uninstall(self, reinstall=False):
    if not reinstall:
        setup_tool = getToolByName(self, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:uninstall')
        registry = setup_tool.getImportStepRegistry()
        fsdSteps = [a['id'] for a in registry.listStepMetadata() if 'Products.FacultyStaffDirectory' in a['handler']]
        for step in fsdSteps:
            registry.unregisterStep(step)