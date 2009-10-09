# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'
# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

import logging
logger = logging.getLogger('FacultyStaffDirectory')
logger.info('Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

import Products.CMFPlone.interfaces
import os
import os.path
from Globals import package_home
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from config import *
DirectoryView.registerDirectory('skins', product_globals)

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry
from Products.FacultyStaffDirectory.tools.FacultyStaffDirectoryTool import FacultyStaffDirectoryTool

def initialize(context):

    # imports packages and types for registration
    import interfaces

    import FacultyStaffDirectory
    import Classification
    import Person
    import Course
    import CommitteesFolder
    import Committee
    import Specialty
    import SpecialtiesFolder
    import PersonGrouping
    import Department
    import CommitteeMembership
    import SpecialtyInformation
    import DepartmentalMembership

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
        for_=Products.CMFPlone.interfaces.IPloneSiteRoot) 
        
    # Register the FacultyStaffDirectory tool    
    cmfutils.ToolInit(
        'Faculty/Staff Directory Tool',
		product_name='FacultyStaffDirectory',
		tools=(FacultyStaffDirectoryTool,),
        icon='skins/FacultyStaffDirectory/group.png').initialize(context)

