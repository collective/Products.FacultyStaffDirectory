import os.path
from App.Common import package_home
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import PRODUCT_DEPENDENCIES, PROJECTNAME
from Products.FacultyStaffDirectory.config import DEPENDENT_PRODUCTS
from Products.FacultyStaffDirectory.config import ADDITIONAL_CATALOG_INDEXES
from Products.FacultyStaffDirectory.config import product_globals as GLOBALS

originalMyFolderActionId = "mystuff"
newMyFolderActionId = "fsdmystuff"
originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"
linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']

def reindexCatlogIndexes(portal, out):
    """
    Reindex the indexes added in generic setup
    """
    portal_catalog = getToolByName(portal, 'portal_catalog')
    for index in ADDITIONAL_CATALOG_INDEXES:
        portal_catalog.manage_reindexIndex(index[0])

def reindexMembrane(portal, out):
    """
    Refresh the membrane_tool catalog. Otherwise, our content disappears from the user db on refresh
    however, rebuilding the entire catalog is a bit excessive, and kills installs on sites with large FSDs, let's do the reindex thing instead
    """
    membraneTool = getToolByName(portal, 'membrane_tool')
    membraneIndexes = membraneTool.indexes()
    membraneTool.manage_reindexIndex(membraneIndexes)

def configureRelations(portal, out):
    """
    configuration for Relations
    """
    relations_tool = getToolByName(portal,'relations_library')
    xmlpath = os.path.join(package_home(GLOBALS),'relations.xml')
    f = open(xmlpath)
    xml = f.read()
    f.close()
    relations_tool.importXML(xml)

def fixMemberAction(portal, out):
    """
    Fixing the 'MemberPrefs' action
    massage the portal_controlpanel tool to make MemberPrefs invisible
    """
    cp = getToolByName(portal, 'portal_controlpanel')
    currentActions = cp.listActions()
    for action in currentActions:
        if action.id == originalProfileActionId:
            action.visible = False

def configureConfiglet(portal, out):
    """
    Register a configlet to control some behaviors of the product:
    TODO: this can be done in generic setup
    """
    cp = getToolByName(portal, 'portal_controlpanel')
    if "FacultyStaffDirectory" not in [ c.id for c in cp._actions ]:
        cp.registerConfiglet(
            "FacultyStaffDirectory",
            "Faculty/Staff Directory",
            "string:${portal_url}/facultystaffdirectory_tool/",
            category="Products",
            permission="Manage portal",
            appId="FacultyStaffDirectory",
            imageUrl="group.png")

def configureVersioning(portal, out):
    """
    Set up revisioning, if available:
    """
    if hasattr(portal,'portal_repository'):
        cp = getToolByName(portal, "portal_repository")
        existing = cp.getVersionableContentTypes()
        new = existing + ['FSDPerson', 'FSDCommittee', 'FSDSpecialty']
        cp.setVersionableContentTypes(new)

def configureKupu(portal, out):
    """
    Does Kupu have a GS setup possibility?  If so, we should absolutely use it.
    """
    def addKupuResource(portal, resourceType, portalType):
        kupu = getToolByName(portal, 'kupu_library_tool')
        resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
        if portalType not in resourceList:
            resourceList.append(portalType)
            kupu.addResourceType(resourceType,tuple(resourceList))
            #ems174: Do we actually need to updateResourceTypes? Kupu gets snippy if we try to add more than one linkable type.
            #kupu.updateResourceTypes(resourceType)
        
    for type in linkableKupuTypes:
        addKupuResource(portal, 'linkable', type)
    for type in mediaKupuTypes:
        addKupuResource(portal, 'mediaobject', type)        
    for type in collectionKupuTypes:
        addKupuResource(portal, 'collection', type)

def unindexTool(portal, out):
    """
    Unindex the FSD tool so it doesn't show up in our folder contents
    """
    # TODO this can be removed once the tool is actually a tool
    fsdTool = getToolByName(portal, 'facultystaffdirectory_tool')
    fsdTool.unindexObject()

def importVarious(context):
    """
    Import various settings.
    """
    portal = context.getSite()
    out = StringIO()
    reindexCatlogIndexes(portal, out)
    reindexMembrane(portal, out)
    configureRelations(portal, out)
    fixMemberAction(portal, out)
    configureConfiglet(portal, out)
    configureVersioning(portal, out)
    configureKupu(portal, out)
    unindexTool(portal, out)
