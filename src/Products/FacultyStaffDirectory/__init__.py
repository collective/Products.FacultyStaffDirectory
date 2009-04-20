# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

import logging
logger = logging.getLogger('FacultyStaffDirectory')
logger.info('Installing Product')

from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils as cmfutils
from config import *

registerDirectory('skins', product_globals)

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

def initialize(context):
    # Register content types with Archetypes
    import FacultyStaffDirectory
    import Person
    import Course
    import PersonGrouping

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])

    profile_registry.registerProfile( 
        name='default', 
        title=PROJECTNAME, 
        description=u'Profile for FacultyStaffDirectory', 
        path='profiles/default', 
        product='FacultyStaffDirectory', 
        profile_type=EXTENSION, 
        for_=IPloneSiteRoot) 
