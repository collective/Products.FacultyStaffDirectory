from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL 
from plone.app.workflow.remap import remap_workflow


def upgrade_2_to_3(context):

    if context.readDataFile('upgrade_2_to_3.txt') is None:
        return

    portal = context.getSite()
    logger = context.getLogger('FacultyStaffDirectory')
    try:
        remap_workflow(portal,
                       ('FSDFacultyStaffDirectory',),
                       ('fsd_directory_workflow',),
                       {})
    except Exception, message:
        logger.error(message)
        raise

    mbtool = getToolByName(portal, MEMBRANE_TOOL)
    mbtool.clearFindAndRebuild()


linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']

def addKupuResource(portal, resourceType, portalType):
    kupu = getToolByName(portal, 'kupu_library_tool')
    resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
    if portalType not in resourceList:
        resourceList.append(portalType)
        kupu.addResourceType(resourceType,tuple(resourceList))

def removeKupuResource(portal, resourceType, portalType):
    kupu = getToolByName(portal, 'kupu_library_tool')
    resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
    if portalType in resourceList:
        resourceList.remove(portalType)
        kupu.addResourceType(resourceType,tuple(resourceList))

def installKupuResources(context):
    """ Add kupu resource types. Kupu's GS handling is broken/nonexistant."""
    portal = context.getSite()
    quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    if quickinstaller.isProductInstalled('kupu'):
        for type in linkableKupuTypes:
            addKupuResource(portal, 'linkable', type)
        for type in mediaKupuTypes:
            addKupuResource(portal, 'mediaobject', type)        
        for type in collectionKupuTypes:
            addKupuResource(portal, 'collection', type)

def uninstallKupuResources(context):
    """Remove Kupu customizations"""
    portal = context.getSite()
    quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    if quickinstaller.isProductInstalled('kupu'):
        for type in linkableKupuTypes:
            removeKupuResource(portal, 'linkable', type)
        for type in mediaKupuTypes:
            removeKupuResource(portal, 'mediaobject', type)
        for type in collectionKupuTypes:
            removeKupuResource(portal, 'collection', type)

TYPES_TO_VERSION = ('FSDPerson', 'FSDCommittee', 'FSDSpecialty')
def setVersionedTypes(context):
    portal = context.getSite()
    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            # use append() to make sure we don't overwrite any
            # content-types which may already be under version control
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)

def removeNavTreeSettings(context):
    """Remove FSD classes from NavTree_properties since this isn't supported
       via GS."""
    portal = context.getSite()
    pprops = getToolByName(portal, 'portal_properties')
    navprops = pprops.navtree_properties
    mtntl = list(navprops.metaTypesNotToList)
    for mType in ['FSDCourse', 'FSDPerson', 'FSDFacultyStaffDirectoryTool']: 
        if mType in list(navprops.metaTypesNotToList):
            mtntl.remove(mType)
    navprops._p_changed=1
    navprops.metaTypesNotToList = tuple(mtntl)
