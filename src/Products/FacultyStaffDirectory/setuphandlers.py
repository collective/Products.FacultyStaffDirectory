import os.path
from App.Common import package_home
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides, noLongerProvides

from Products.FacultyStaffDirectory.adapters.tree import personGroupingTree
from Products.FacultyStaffDirectory.config import ADDITIONAL_CATALOG_INDEXES, product_globals as GLOBALS
from Products.FacultyStaffDirectory.interfaces import IPersonGrouping, ITree, IConfiguration, ISiteMarker
from Products.FacultyStaffDirectory.utilities import ConfigurationUtility

def reindexCatalogIndexes(portal):
    """Reindex the indexes added in generic setup"""
    portal_catalog = getToolByName(portal, 'portal_catalog')
    for index in ADDITIONAL_CATALOG_INDEXES:
        portal_catalog.manage_reindexIndex(index[0])

def reindexMembrane(portal):
    """Refresh the membrane_tool catalog. Otherwise, our content disappears from the user db on refresh.
    
    However, rebuilding the entire catalog is a bit excessive, and kills installs on sites with large FSDs; let's do the reindex thing instead.
    
    """
    membraneTool = getToolByName(portal, 'membrane_tool')
    membraneIndexes = membraneTool.indexes()
    membraneTool.manage_reindexIndex(membraneIndexes)

def fixMemberAction(portal):
    """Massage the portal_controlpanel tool to make the MemberPrefs action invisible."""
    cp = getToolByName(portal, 'portal_controlpanel')
    currentActions = cp.listActions()
    for action in currentActions:
        if action.id == "MemberPrefs":  # MemberPrefs is the stock action ID.
            action.visible = False

def configureVersioning(portal):
    """Set up revisioning, if available:"""
    if hasattr(portal,'portal_repository'):
        cp = getToolByName(portal, "portal_repository")
        existing = cp.getVersionableContentTypes()
        new = existing + ['FSDPerson']
        cp.setVersionableContentTypes(new)

def configureKupu(portal):
    """Does Kupu have a GS setup possibility?  If so, we should absolutely use it."""
    def addKupuResource(portal, resourceType, portalType):
        kupu = getToolByName(portal, 'kupu_library_tool')
        resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
        if portalType not in resourceList:
            resourceList.append(portalType)
            kupu.addResourceType(resourceType,tuple(resourceList))
            #ems174: Do we actually need to updateResourceTypes? Kupu gets snippy if we try to add more than one linkable type.
            #kupu.updateResourceTypes(resourceType)
        
    linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDPersonGrouping']
    mediaKupuTypes = ['FSDPerson']
    collectionKupuTypes = ['FSDFacultyStaffDirectory']
    
    for type in linkableKupuTypes:
        addKupuResource(portal, 'linkable', type)
    for type in mediaKupuTypes:
        addKupuResource(portal, 'mediaobject', type)        
    for type in collectionKupuTypes:
        addKupuResource(portal, 'collection', type)

def registerConfigurationUtility(portal):
    """Register the utility that holds FSD's configuration settings at the root of the Plone site."""
    portal.getSiteManager().registerUtility(ConfigurationUtility(), provided=IConfiguration)
    # Is automatically uninstalled by QuickInstaller. Local adapters aren't, oddly enough.
    
def registerTreeAdapters(portal):
    """Register the adapters for various content types to the ITree interface."""
    sm = portal.getSiteManager()
    sm.registerAdapter(personGroupingTree, required=(IPersonGrouping,), provided=ITree)

def applyMarkerInterface(portal):
    """Apply a marker interface to the Plone site. Our ++fsdmembership++ traverser uses it to limit itself to sites where FSD is actually installed."""
    alsoProvides(portal, ISiteMarker)

def importVarious(context):
    """Import various settings."""
    portal = context.getSite()
    reindexCatalogIndexes(portal)
    reindexMembrane(portal)
    fixMemberAction(portal)
    configureVersioning(portal)
    configureKupu(portal)
    registerConfigurationUtility(portal)
    registerTreeAdapters(portal)
    applyMarkerInterface(portal)
    # And just drop `out` on the floor, apparently.


# Uninstallation:

def ditchMarkerInterface(portal):
    """Remove the FSD-is-installed marker interface from the Plone site."""
    noLongerProvides(portal, ISiteMarker)

def uninstall(context):
    """Undo what's done in importVarious that GS doesn't automatically undo."""
    portal = context.getSite()
    ditchMarkerInterface(portal)
