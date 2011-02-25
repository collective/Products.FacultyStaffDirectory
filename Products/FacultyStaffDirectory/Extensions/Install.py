# -*- coding: utf-8 -*-
from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import PROJECTNAME


__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'


originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"

def install(self, reinstall=False):
    """ External Method to install FacultyStaffDirectory """
    
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    def importProfiles(self, importContexts):
        """Import all steps from the GenericSetup profiles listen in `importContexts`."""
        setupTool = getToolByName(self, 'portal_setup')
        for eachContext in importContexts:
            setupTool.runAllImportStepsFromProfile(eachContext)

    profilesToImport = ('profile-Products.FacultyStaffDirectory:default',)

    importProfiles(self, profilesToImport)

    print >> out, "Ran all GS import steps." 
    
    #####
    # Action Manipulations
    #   These should probably also live in GS profiles, eventually.  Move them there if possible
    #   This should be movable after we drop support for plone 2.5
        
    # Fixing the 'MemberPrefs' action
    # massage the portal_controlpanel tool to make MemberPrefs invisible
    cp = getToolByName(self, 'portal_controlpanel')
    currentActions = cp.listActions()
    for action in currentActions:
        if action.id == originalProfileActionId:
            action.visible = False

    # Unindex the FSD tool so it doesn't show up in our folder contents
    fsdTool = getToolByName(self, 'facultystaffdirectory_tool')
    fsdTool.unindexObject()
    
    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()
    
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:uninstall')
        
    # don't do things we don't need to do on reinstall
    if not reinstall:
        # massage the portal_controlpanel tool to make MemberPrefs visible
        # at the same time, delete the action we created via GS Profile
        cp = getToolByName(self, 'portal_controlpanel')
        currentActions = cp.listActions()
        index = 0
        for action in currentActions:
            if action.id == originalProfileActionId:
                action.visible = True
            if action.id == newProfileActionId:
                cp.deleteActions([index])
            index += 1
        
        # Okay, unregister the membrane_tool from the InstalledProduct.portalobjects property in the QI tool.
        # IMPORTANT!!!
        # remember that this is all because of the way we are installing membrane in the 
        # first place, when the QI tool is improved in all versions to support installing 
        # via GS profile alone, this will be moot.  It shouldn't break even then, though, 
        # # because of the set stuff.
        # qt = getToolByName(self, 'portal_quickinstaller')
        # fsd_product = getattr(qt, 'FacultyStaffDirectory')
        # portal_objects_list = fsd_product.getPortalObjects()
        # pol_set = set(portal_objects_list)
        # removal_set = set([MEMBRANE_TOOL])
        # fsd_product.portalobjects = tuple(pol_set - removal_set)

    return out.getvalue()
