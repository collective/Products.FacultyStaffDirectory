# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import View, ManageProperties, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFCore.permissions import ManageUsers
from Products.membrane.interfaces import IPropertiesProvider
from Products.FacultyStaffDirectory.interfaces import IClassification
from Products.FacultyStaffDirectory.permissions import ASSIGN_CLASSIFICATIONS_TO_PEOPLE

schema = Schema((

    RelationField(
        name='people',
        widget=ReferenceBrowserWidget(
            label=u'People',
            label_msgid='FacultyStaffDirectory_label_people',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type':'FSDPerson', 'sort_on':'getSortableName'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,            
        ),
        write_permission=ASSIGN_CLASSIFICATIONS_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=1,
        relationship='classifications_people'
    ),
),
)

Classification_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Classification(PersonGrouping):
    """A group of people like Faculty, Staff, or Grad Students"""
    security = ClassSecurityInfo()
    meta_type = portal_type = "FSDClassification"
    # zope3 interfaces
    implements(IClassification, IPropertiesProvider)
    _at_rename_after_creation = True
    schema = Classification_schema
    # set the relationship of this grouping to FSDPeople as a property
    relationship = 'classifications_people'

registerType(Classification, PROJECTNAME)
