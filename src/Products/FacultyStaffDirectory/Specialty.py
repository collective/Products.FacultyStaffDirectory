# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.interfaces import ISpecialty
from Products.FacultyStaffDirectory.permissions import ASSIGN_SPECIALTIES_TO_PEOPLE

from zope.interface import implements

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
        write_permission=ASSIGN_SPECIALTIES_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=True,
        relationship='SpecialtyInformation'  # weird relationship name is ArchGenXML's fault
    ),

    ImageField(
        name='overviewImage',
        schemata='Overview',
        widget=ImageWidget(
            label=u"Overview image (used for specialty overview view)",
            label_msgid='FacultyStaffDirectory_label_overview_image',
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage=AttributeStorage(),
        original_size=(200, 200),
        sizes={'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),

    TextField(
        name='overviewText',
        schemata='Overview',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=u"Overview text (used for specialty overview view)",
            label_msgid='FacultyStaffDirectory_label_overview_text',
            i18n_domain='FacultyStaffDirectory',
        ),
        default_output_type="text/x-html-safe",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',)
    )

),
)

Specialty_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Specialty(PersonGrouping):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(PersonGrouping,'__implements__',()),)
    implements(ISpecialty)
    meta_type = portal_type = 'FSDSpecialty'
    _at_rename_after_creation = True
    schema = Specialty_schema
    relationship = 'SpecialtyInformation'
    
    # Methods
    security.declareProtected(View, 'getSpecialtyInformation')
    def getSpecialtyInformation(self, person):
        """
        Get the specialty information for a specific person
        """
        refCatalog = getToolByName(self, 'reference_catalog')
        refs = refCatalog.getReferences(self, 'SpecialtyInformation', person)

        if refs:
            return refs[0].getContentObject()
        else:
            return None

registerType(Specialty, PROJECTNAME)
