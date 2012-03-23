import os.path
import logging
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.FacultyStaffDirectory.config import product_globals as GLOBALS
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']
logger = logging.getLogger("Products.FacultyStaffDirectory")

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
    if context.readDataFile('installKupuResources.txt') is None:
        return
    portal = context.getSite()
    quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    if quickinstaller.isProductInstalled('kupu'):
        for type in linkableKupuTypes:
            addKupuResource(portal, 'linkable', type)
        for type in mediaKupuTypes:
            addKupuResource(portal, 'mediaobject', type)
        for type in collectionKupuTypes:
            addKupuResource(portal, 'collection', type)

def installRelationsRules(context):
    if context.readDataFile('installRelationsRules.txt') is None:
        return
    portal = context.getSite()
    relations_tool = getToolByName(portal,'relations_library')
    xmlpath = os.path.join(package_home(GLOBALS),'relations.xml')
    f = open(xmlpath)
    xml = f.read()
    f.close()
    relations_tool.importXML(xml)

def uninstallKupuResources(context):
    """Remove Kupu customizations"""
    if context.readDataFile('uninstallKupuResources.txt') is None:
        return
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
def installVersionedTypes(context):
    if context.readDataFile('installVersionedTypes.txt') is None:
        return
    try:
        from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
    except ImportError:
        # Use repositorytool.xml instead (Plone 4.1 and above)
        pass
    else:
        portal = context.getSite()
        portal_repository = getToolByName(portal, 'portal_repository')
        versionable_types = list(portal_repository.getVersionableContentTypes())
        for type_id in TYPES_TO_VERSION:
            if type_id not in versionable_types:
                # use append() to make sure we don't overwrite any
                # content-types which may already be under version control
                versionable_types.append(type_id)
                for policy_id in DEFAULT_POLICIES:
                    portal_repository.addPolicyForContentType(type_id, policy_id)
        portal_repository.setVersionableContentTypes(versionable_types)

def uninstallNavTreeSettings(context):
    """Remove FSD classes from NavTree_properties since this isn't supported
       via GS."""
      
    if context.readDataFile('uninstallNavTreeSettings.txt') is None:
        return
    portal = context.getSite()
    pprops = getToolByName(portal, 'portal_properties')
    navprops = pprops.navtree_properties
    mtntl = list(navprops.metaTypesNotToList)
    for mType in ['FSDCourse', 'FSDPerson', 'FSDFacultyStaffDirectoryTool']:
        if mType in list(navprops.metaTypesNotToList):
            mtntl.remove(mType)
    navprops._p_changed=1
    navprops.metaTypesNotToList = tuple(mtntl)


def uninstallConfiglet(context):
    """ Remove the FSD control panel item"""

    if context.readDataFile('uninstallNavTreeSettings.txt') is None:
        return
    portal = context.getSite()
    cp = getToolByName(portal, 'portal_controlpanel')
    cp.unregisterApplication('FacultyStaffDirectory')

def unindexFSDTool(context):
    """ Unindex the FSD tool so it doesn't show up in folder contents"""
    if context.readDataFile('unindexFSDTool.txt') is None:
        return
    portal = context.getSite()
    fsdTool = getToolByName(portal, 'facultystaffdirectory_tool')
    fsdTool.unindexObject()

originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"
def hideMemberPrefs(context):
       # Fixing the 'MemberPrefs' action
       # massage the portal_controlpanel tool to make MemberPrefs invisible
       if context.readDataFile('hideMemberPrefs.txt') is None:
           return
       portal = context.getSite()
       cp = getToolByName(portal, 'portal_controlpanel')
       currentActions = cp.listActions()
       for action in currentActions:
           if action.id == originalProfileActionId:
               action.visible = False

def restoreMemberPrefs(context):
    """Massage the portal_controlpanel tool to make MemberPrefs visible
    at the same time, delete the action we created via GS Profile"""
    if context.readDataFile('restoreMemberPrefs.txt') is None:
        return
    portal = context.getSite()
    cp = getToolByName(portal, 'portal_controlpanel')
    currentActions = cp.listActions()
    index = 0
    for action in currentActions:
        if action.id == originalProfileActionId:
            action.visible = True
        if action.id == newProfileActionId:
            cp.deleteActions([index])
        index += 1

def reindexFSDObjects(context):
    """Update indexes relevant to FSD objects"""
    if context.readDataFile('reindexFSDObjects.txt') is None:
        return
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    INDEX_LIST = ['getSortableName', 'getRawClassifications',
                  'getRawSpecialties', 'getRawCommittees',
                  'getRawDepartments', 'getRawPeople']
    for index in INDEX_LIST:
        catalog.reindexIndex(index, None)
    membrane = getToolByName(portal, MEMBRANE_TOOL)
    membrane.refreshCatalog()

# ################## #
#   sample-content   #
# ################## #

def addSampleContent(portal):
    logger.info("Starting to add %s sample-content." % GLOBALS['PROJECTNAME'])
    # Gather up all our tools.
    portal_workflow = getToolByName(portal, 'portal_workflow')
    # Add a directory.
    directory_id = 'directory'
    if directory_id not in portal:
        directory = _createObjectByType(
            'FSDFacultyStaffDirectory', portal,
            id=directory_id,
            title="Faculty and Staff Directory",
            )
        portal_workflow.doActionFor(directory, 'publish')
        info_msg = "Added a directory (%s)."
    else:
        directory = portal[directory_id]
        info_msg = "Using existing directory (%s)."
    logger.info(info_msg % directory)

    # Add classifications.
    classifications = {}
    classification_ids = ('faculty', 'staff', 'graduate-students',)
    for classification_id in classification_ids:
        if classification_id not in directory:
            title = classification_id.replace('-', ' ').title()
            classification = _createObjectByType(
                'FSDClassification', directory,
                id=classification_id,
                title=title,
                )
            # NOTE classifications are defaulted to an active state,
            #      therefore no workflow transition is necessary here.
            info_msg = "Added a classification (%s)."
        else:
            classification = directory[classification_id]
            info_msg = "Using existing classification (%s)."
        # Capture classification for later use with people.
        classifications[classification_id] = classification
        logger.info(info_msg % classification)

    # Add a committees container.
    committees_container_id = 'committees'
    if committees_container_id not in directory:
        title = committees_container_id.title()
        committees_container = _createObjectByType(
            'FSDCommitteesFolder', directory,
            id=committees_container_id,
            title=title,
            )
        info_msg = "Added a committees folder (%s)."
    else:
        committees_container = directory[committees_container_id]
        info_msg = "Using existing committees folder (%s)."
    logger.info(info_msg % committees_container)
    # Add committees to the committee container.
    committees = {}
    committee_ids = ('climate-and-diversity', 'technology-roundtable',)
    for committee_id in committee_ids:
        if committee_id not in committees_container:
            title = committee_id.replace('-', ' ').title()
            committee = _createObjectByType(
                'FSDCommittee', committees_container,
                id=committee_id,
                title=title,
                )
            info_msg = "Added committee (%s)."
        else:
            committee = committees_container[committee_id]
            info_msg = "Using existing committee (%s)."
        committees[committee_id] = committee
        logger.info(info_msg % committee)

    # Add a specialties folder.
    specialties_container_id = 'specialties'
    if specialties_container_id not in directory:
        title = specialties_container_id.title()
        specialties_container = _createObjectByType(
            'FSDSpecialtiesFolder', directory,
            id=specialties_container_id,
            title=title,
            )
        info_msg = "Added a specialties folder (%s)."
    else:
        specialties_container = directory[specialties_container_id]
        info_msg = "Using existing specialties folder (%s)."
    logger.info(info_msg % specialties_container)

    # Add people to the directory.
    people_info = (
        dict(id='abc123',
             firstName='Abe', middleName='Bob', lastName='Crumpt',
             suffix='Ph.D. EPT',
             password='abe',
             email='abe@example.com',
             classifications=(classifications['faculty'].UID(),),
             committees=(committees['climate-and-diversity'].UID(),),
             ),
        )
    for person_info in people_info:
        id = person_info['id']
        if id not in directory:
            pass
            person = _createObjectByType(
                'FSDPerson', directory,
                **person_info)
            info_msg = "Added a person (%s)."
        else:
            person = directory[id]
            info_msg = "Using existing person (%s)."
        logger.info(info_msg % person)
        # NOTE There is no reason to transition workflow on a person.
        #      By default people are initialized to a visable state.

def importSampleContent(context):
    # Only run step if a flag file is present
    if context.readDataFile('Products.FacultyStaffDirectory-sample-content.txt') is None:
        return
    addSampleContent(context.getSite())
