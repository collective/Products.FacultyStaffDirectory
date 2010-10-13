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

    mbtool = getToolByName(context, MEMBRANE_TOOL)
    mbtool.clearFindAndRebuild()
