from Products.CMFCore.utils import getToolByName
from plone.app.workflow.remap import remap_workflow
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL 

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
