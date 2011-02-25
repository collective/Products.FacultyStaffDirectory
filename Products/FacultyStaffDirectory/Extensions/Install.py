# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'
import sys
from StringIO import StringIO
from sets import Set
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.atapi import listTypes
from Products.FacultyStaffDirectory.config import PROJECTNAME
from Products.FacultyStaffDirectory.config import product_globals as GLOBALS
from Products.FacultyStaffDirectory.config import ADDITIONAL_CATALOG_INDEXES
from Products.FacultyStaffDirectory.config import ADDITIONAL_CATALOG_METADATA
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

originalMyFolderActionId = "mystuff"
newMyFolderActionId = "fsdmystuff"
originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"

def install(self, reinstall=False):
    """ External Method to install FacultyStaffDirectory """
    
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    
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
        
    # Fixing the 'MyFolder' action
    # massage the membership tool actions to make 'mystuff' invisible,
    # This allows the one we added in GS to take its place silently.
    actionsTool = getToolByName(self, 'portal_actions')
    actions = actionsTool.listActions()
    for action in actions:
        if action.id == originalMyFolderActionId:
            action.visible = False
    
    # now move the new my folder action up to the top of the list
    orderedFolder = actionsTool.user
    orderedFolder.manage_move_objects_to_top(None,(newMyFolderActionId,))
        
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
    
        # uninstall the vcard action icon
        ai=getToolByName(self, 'portal_actionicons')
        try:
            ai.removeActionIcon('plone', 'vcard')
        except KeyError:
            #Icon doesn't exist, problem solved.
            pass
        
        # massage the membership tool actions to make 'mystuff' visible,
        # at the same time, remove the action we created via GS profile
        tool = getToolByName(self, 'portal_actions')
        currentActions = tool.listActions()
        index = 0
        for action in currentActions:
            if action.id == originalMyFolderActionId:
                action.visible = True
            if action.id == newMyFolderActionId:
                tool.deleteActions([index])
            index += 1
        
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
        # because of the set stuff.
        qt = getToolByName(self, 'portal_quickinstaller')
        fsd_product = getattr(qt, 'FacultyStaffDirectory')
        portal_objects_list = fsd_product.getPortalObjects()
        pol_set = set(portal_objects_list)
        removal_set = set([MEMBRANE_TOOL])
        fsd_product.portalobjects = tuple(pol_set - removal_set)

    return out.getvalue()
