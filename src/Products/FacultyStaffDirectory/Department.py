# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import View
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.interfaces import IDepartment
from zope.interface import implements
from Products.FacultyStaffDirectory.permissions import ASSIGN_DEPARTMENTS_TO_PEOPLE

schema = Schema((

    RelationField(
        name='people',
        widget=ReferenceBrowserWidget(
            label=u'Members',
            label_msgid='FacultyStaffDirectory_label_members',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type':'FSDPerson', 'sort_on':'getSortableName'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,            
        ),
        write_permission=ASSIGN_DEPARTMENTS_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=1,
        relationship='departments_members'
    ),
),
)

Department_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Department(PersonGrouping):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(PersonGrouping,'__implements__',()),)
    implements(IDepartment)
    _at_rename_after_creation = True
    meta_type = portal_type="FSDDepartment"
    schema = Department_schema   
    relationship = 'departments_members'
    
    # Methods
    security.declareProtected(View, 'getMembershipInformation')
    def getMembershipInformation(self, person):
        """ Get the departmental membership information for a specific person
        """
        refCatalog = getToolByName(self, 'reference_catalog')
        refs = refCatalog.getReferences(self, 'departments_members', person)

        if not refs:
            return None
        else:
            return refs[0].getContentObject()
        
registerType(Department, PROJECTNAME)
