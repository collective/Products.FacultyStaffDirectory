from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL, ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.interfaces import ICategoryMapper
from Products.FacultyStaffDirectory import MEMBRANE_ABLE_TYPES, MEMBRANE_TYPE_ACTIVE_STATES

def modifyMembraneTypes(event):
    """Check facultystaffdirectory_tool schemata,
       switch on/off membrane types based on the information we find there.
    """
    context = event.context
    mbtool = getToolByName(context, MEMBRANE_TOOL)
    enable_types = context.getEnableMembraneTypes()
    current_types = mbtool.listMembraneTypes()
    changed_something = False

    for type in MEMBRANE_ABLE_TYPES:
        if type in enable_types:
            if type not in current_types:
                # register the type
                mbtool.registerMembraneType(type)
                # re-establish the active status map for the type
                mapper = ICategoryMapper(mbtool)
                cat_set = generateCategorySetIdForType(type)
                states = MEMBRANE_TYPE_ACTIVE_STATES[type]
                mapper.replaceCategoryValues(cat_set, ACTIVE_STATUS_CATEGORY, states)
                changed_something = True
        else:
            if type in current_types:
                mbtool.unregisterMembraneType(type)
                changed_something = True
    
    if changed_something:
        mbtool.clearFindAndRebuild()
